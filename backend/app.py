from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from .rag.answering_engine import add_document, get_answer
import tempfile

class QuestionModel(BaseModel):
    document_id: str
    question: str

app = FastAPI()

@app.post('/answer_question')
async def answer_question(req: QuestionModel):
    return {'answer': get_answer(req.question, req.document_id)}


@app.post('/upload_document')
async def upload_document(file: UploadFile):
    with tempfile.NamedTemporaryFile(suffix=file.filename) as tmp:
        tmp.write(file.file.read())
        return {'document_id': add_document(tmp.name)}