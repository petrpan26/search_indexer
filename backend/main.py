from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from .rag.answering_engine import add_document, get_answer
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import nltk
from dotenv import load_dotenv
import os
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from fastapi_cache.backends.inmemory import InMemoryBackend

load_dotenv()  # take environment variables from .env.
FastAPICache.init(backend= InMemoryBackend())

class QuestionModel(BaseModel):
    document_id: str
    question: str



app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

origins = [os.environ.get('CLIENT_URL', 'http://localhost:3000')]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

nltk.download('punkt')

@app.post('/api/answer_question')
async def answer_question(req: QuestionModel):
    return {'answer': get_answer(req.question, req.document_id)}


@app.post('/api/upload_document')
async def upload_document(file: UploadFile):
    with tempfile.NamedTemporaryFile(suffix=file.filename) as tmp:
        tmp.write(file.file.read())
        return {'document_id': add_document(tmp.name)}
    
@app.get('/api/test')
async def test():
    return {'response': 'This test fail succesfully'}