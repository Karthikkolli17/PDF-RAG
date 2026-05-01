from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from vector import query
from generate import generate

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def index():
    return FileResponse("static/index.html")


@app.post("/chat")
def chat(request: ChatRequest):
    results = query(request.message)
    answer = generate(request.message, results)
    sources = [
        {"page": m.get("page", "?"), "type": m.get("type", ""), "course": m.get("course_code", "")}
        for m in results["metadatas"][0]
    ]
    return {"answer": answer, "sources": sources}
