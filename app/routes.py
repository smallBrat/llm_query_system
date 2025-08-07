# app/routes.py

from fastapi import APIRouter, HTTPException, Header, Request
from pydantic import BaseModel
from app.pipeline import process_document_and_questions

router = APIRouter()

# Request schema
class RunRequest(BaseModel):
    documents: str
    questions: list[str]

@router.post("/hackrx/run")
async def run_hackrx_api(
    request: RunRequest,
    authorization: str = Header(None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    try:
        answers = process_document_and_questions(request.documents, request.questions)
        return {"answers": answers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
