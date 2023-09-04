from fastapi import APIRouter
from dotenv import load_dotenv
from pydantic import BaseModel
import openai
import os
import json

load_dotenv()

openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_KEY")

class Prompt(BaseModel):
    msg: str

router = APIRouter(
    prefix="/questionario",
    tags=["questionario"],
    responses={404: {"description": "Not found"}}
)

@router.post("/")
async def questionario(prompt: Prompt):
     
    print(prompt.msg)   
     
    questionariogpt = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Elabore questionários com base no tema fornecido pelo usuário, utilizando 1 enunciado e 4 alternativas (A, B, C, D) para cada pergunta. Certifique-se de que a resposta correta seja calculada corretamente e não seja igual à expressão da pergunta."},
            {"role": "system", "content": 'Use o formato: {"questionario":[{"alternativas":{"a":"Texto da alternativa A","b":"Texto da alternativa B","c":"Texto da alternativa C","d":"Texto da alternativa D"},"enunciado":"Enunciado da pergunta?","resposta":"a"}]}.'},
            {"role": "system", "content": "Responda apenas no formato JSON, sem comentários pessoais. Seja sucinto nas alternativas, evitando repetir o enunciado na resposta."},
            {"role": "system", "content": "Cada pergunta deve ter apenas uma resposta correta."},
            {"role": "system", "content": "Não responda como chat, apenas devolva o modelo. Use sempre o formato JSON especificado para todas as respostas geradas pelo GPT."},
            {"role": "user", "content": prompt.msg}

        ]
    )
    
    result = questionariogpt.choices[0].message.content
    print(result)
    result_json = json.loads(result)
    
    return { "response" : result_json }

@router.get("/{id}")
async def get_questionario(id: int):
    multi = id**2
    return { "message" : multi }
