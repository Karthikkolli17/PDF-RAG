import logging
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, field_validator
from vector import query
from generate import generate, deflect
from planner import plan

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("chat")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


class ChatRequest(BaseModel):
    message: str

    @field_validator("message")
    @classmethod
    def message_length(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("message cannot be empty")
        if len(v) > 2000:
            raise ValueError("message too long (max 2000 characters)")
        return v


@app.get("/")
def index():
    return FileResponse("static/index.html")


@app.post("/chat")
def chat(request: ChatRequest):
    msg = request.message
    try:
        p = plan(msg)
    except Exception as e:
        log.error("plan failed: %s | msg=%r", e, msg)
        raise HTTPException(status_code=500, detail="We couldn't understand that. Please try rephrasing.")

    intent = p.get("intent")
    log.info("plan intent=%s depts=%s progs=%s codes=%s ambig=%s",
             intent, p.get("departments"), p.get("programs"),
             p.get("course_codes"), p.get("is_ambiguous"))

    if intent == "out_of_scope":
        return {"answer": deflect(msg), "sources": [], "plan": p}

    if p.get("is_ambiguous"):
        clarification = p.get("clarification") or "Could you be more specific about what you're asking?"
        return {"answer": clarification, "sources": [], "plan": p}

    try:
        results = query(msg, plan_dict=p)
        answer = generate(msg, results, plan=p)
    except Exception as e:
        log.error("retrieve/generate failed: %s | msg=%r | intent=%s", e, msg, intent)
        raise HTTPException(status_code=500, detail="Something went wrong while answering. Please try again.")

    sources = [
        {"page": m.get("page", "?"), "type": m.get("type", ""), "course": m.get("course_code", "")}
        for m in results["metadatas"][0]
    ]
    return {"answer": answer, "sources": sources, "plan": p}
