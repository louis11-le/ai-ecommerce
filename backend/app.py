from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()


import uvicorn
from agents.router_agent import route_query
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or use ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Query(BaseModel):
    question: str


@app.post("/ask")
async def ask_question(query: Query):
    user_input = query.question
    response = route_query(user_input)
    return {"answer": response}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
