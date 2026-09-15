from fastapi import FastAPI
from pydantic import BaseModel

from backend.telecom_billing_agent_litellm_app import investigate_billing


app = FastAPI(
    title="Telecom Billing Investigation Agent",
    description="Backend API for the telecom billing investigation agent",
    version="1.0.0"
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    response = investigate_billing(
        request.message
    )

    return {
        "response": response
    }