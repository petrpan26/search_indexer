from openai import OpenAI
from fastapi import HTTPException
import openai

OPEN_AI_EMBEDDING_MODEL = 'text-embedding-ada-002'
client = OpenAI()

def fetch_embeddings(texts: list[str]) -> list[list[float]]:
    try:
        results =  client.embeddings.create(input = texts, model=OPEN_AI_EMBEDDING_MODEL).data
        embeddings = [result.embedding 
                    for result in results]
        return embeddings
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