from nltk.tokenize import sent_tokenize
from backend.file_helper import read_document_from_file
from openai import OpenAI
import uuid
from pinecone import Index
from fastapi import HTTPException

client = OpenAI()
OPEN_AI_EMBEDDING_MODEL = 'text-embedding-ada-002'
index = Index("document_indexer")

# Split document into paragraph of roughly of max_char size
def split_document_to_paragraphs(document: str, paragraph_len: int = 500) -> list[str]:
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

def fetch_open_ai_embeddings(texts: list[str]) -> list[list[float]]:
    try:
        embeddings = [result['embedding'] 
                    for result in client.embeddings.create(input = paragraphs, model=OPEN_AI_EMBEDDING_MODEL)['data']]
        return embeddings
    except Exception as e:
        raise HTTPException(404, detail= f'OpenAI embedding fetch fail with error {e}')

def add_document_to_pinecone(document_id: str, paragraphs: list[str], embeddings: list[str]):
    try:
        Index.upsert(
            vectors=[
                (
                f"{document_id}_{i}", # Id of vector
                embedding ,  # Dense vector values
                {"document_id": document_id, "sentence_id": i, "text": paragraph} 
                # For ease of architecture I will save the text in pinecone as well
                # This is not recommended since Pinecone memory might be expensive
                )
                for i, (paragraph, embedding) in enumerate(zip(paragraphs, embeddings)) 
            ]
        )
    except Exception as e:
        raise HTTPException(404, detail= f'Pinecone indexing fetch fail with error {e}')

# Add document to the database and return id of the document
def add_document(filepath: str) -> str:
    document_text = read_document_from_file(filepath)
    paragraphs = split_document_to_paragraphs(document_text)
    embeddings = fetch_open_ai_embeddings(paragraphs)
    document_id = uuid.uuid4()
    add_document_to_pinecone(document_id, paragraphs, embeddings)
    return document_id

def get_answer(question: str, document_id: str):
    embedding = fetch_open_ai_embeddings([question])[0]

    query_response = index.query(
        top_k=3,
        vector=embedding,
        filter={
            "document_id": {"$eq": document_id},
        },
        include_metadata=True
    )
    answers = [q['metadata']['text'] for q in query_response['matches'] if q['score']]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": 
                 f"""
    The answer to this question "{question}" are in the following sentences generate just the answer plus the reasoning of the answer in one line. Answer the question in the language of the question. If there are no answer just output the word "None"
    {str(answers)}
                 """.strip()}
        ],
        temperature = 0
    )
    answer = response.choices[0].message.content
    print(f"Price: {response.usage.total_tokens * 0.003 / 1000} $")
    reasoning = None
    if answer != 'None':
        reasoning = answers[0]
    return answer
    




    