# backend/rag/llm.py
from openai import OpenAI
from fastapi import HTTPException
import cohere
import os

client = OpenAI()
co = cohere.Client(api_key=os.environ.get('COHERE_API_KEY'))

COHERE_EMBEDDING_MODEL = 'embed-english-v3.0'

def fetch_embeddings(texts: list[str], embedding_type: str = 'search_document') -> list[list[float]]:
    try:
        results =  co.embed(
            texts=texts,
            model=COHERE_EMBEDDING_MODEL,
            input_type=embedding_type
        ).embeddings
        return results
    except Exception as e:
        print(e)
        raise HTTPException(404, detail= f'OpenAI embedding fetch fail with error {e}')

def question_and_answer_prompt(question: str, context: list[str]) -> str:
    context_str = '\n'.join(context)
    return f"""
    Context information is below.
    ---------------------
    {context_str}
    ---------------------
    Given the context information and not prior knowledge, answer the query.
    Query: {question}
    Answer: 
    """

def synthesize_answer(question: str, context: list[str]) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": question_and_answer_prompt(question, context)}
        ],
        temperature=0
    )
    answer = response.choices[0].message.content
    print(f"Price: {response.usage.total_tokens * 0.003 / 1000} $")
    return answer