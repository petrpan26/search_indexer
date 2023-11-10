import pinecone
from pinecone.core.client.configuration import Configuration as OpenApiConfiguration
from fastapi import HTTPException
import os

PINECONE_ENVIRONMENT = os.environ.get('PINECONE_ENV') if  os.environ.get('PINECONE_ENV') is not None else 'gcp-starter'
TOP_K_DOCUMENTS = 3
INDEX_NAME = 'document-indexer'

openapi_config = OpenApiConfiguration.get_default_copy()
pinecone.init(
    api_key=os.environ.get('PINECONE_API_KEY'), 
    environment=PINECONE_ENVIRONMENT,
    openapi_config=openapi_config)



if INDEX_NAME not in pinecone.list_indexes():
    pinecone.create_index(INDEX_NAME, dimension=1536, metadata_config={"indexed": ["document_id"]})

index = pinecone.Index(INDEX_NAME)

def add_document_to_db(document_id: str, paragraphs: list[str], embeddings: list[str]):
    try:
        index.upsert(
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
    
def fetch_top_paragraphs(document_id: str, embedding: list[float]) -> list[str]:
    try:
        query_response = index.query(
            top_k=TOP_K_DOCUMENTS,
            vector=embedding,
            filter={
                "document_id": {"$eq": document_id},
            },
            include_metadata=True
        )
    except Exception as e:
        raise HTTPException(404, detail= f'Pinecone indexing fetch fail with error {e}')
    
    answers = [q['metadata']['text'] for q in query_response['matches']]
    return answers 