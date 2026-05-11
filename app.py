from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, field_validator
from vector import query
from generate import generate

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
    try:
        results = query(request.message)
        answer = generate(request.message, results)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to process your request. Please try again.")
    sources = [
        {"page": m.get("page", "?"), "type": m.get("type", ""), "course": m.get("course_code", "")}
        for m in results["metadatas"][0]
    ]
    return {"answer": answer, "sources": sources}
