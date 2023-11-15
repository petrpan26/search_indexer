# backend/rag/answering_engine.py
from nltk.tokenize import sent_tokenize
from .file_helper import read_document_from_file
import uuid
from .llm import fetch_embeddings, synthesize_answer
from .vectordb import add_document_to_db, fetch_top_paragraphs
from fastapi import HTTPException

# Split document into paragraph of roughly of max_char size
def split_document_to_paragraphs(document: str, paragraph_len: int = 1000) -> list[str]:
    sentences = sent_tokenize(document) # Split the paragraph by sentences

    paragraphs = []
    paragraph = ''
    for sentence in sentences:
        paragraph += ' ' + sentence
        if len(paragraph) >= paragraph_len:
            paragraphs.append(paragraph)
            paragraph = ''

    if len(paragraph) > 0:
        paragraphs.append(paragraph)
    
    return paragraphs

# Add document to the database and return id of the document
def add_document(filepath: str) -> str:
    document_text = read_document_from_file(filepath)
    paragraphs = split_document_to_paragraphs(document_text)
    if len(paragraphs) == 0:
        raise HTTPException('404', detail='No text was extracted from the document')
    embeddings = fetch_embeddings(paragraphs, embedding_type='search_document')
    document_id = str(uuid.uuid4())
    add_document_to_db(document_id, paragraphs, embeddings)
    print(document_id)
    return document_id

def get_answer(question: str, document_id: str):
    embedding = fetch_embeddings([question], embedding_type='search_query')[0]
    relevant_paragraphs = fetch_top_paragraphs(document_id, embedding)
    if len(relevant_paragraphs) == 0:
        raise HTTPException(404, detail='Embedding are not ready yet for this document')
    return synthesize_answer(question, relevant_paragraphs)
    




    