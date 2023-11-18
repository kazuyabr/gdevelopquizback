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
            {"role": "system", "content": "Elabore questionários com base no tema fornecido pelo usuário, utilizando 1 enunciado e 4 alternativas para cada pergunta. Certifique-se de que as alternativas de resposta sejam completamente corretas e adequadas à pergunta. Varie a letra da alternativa correta (a, b, c ou d) de forma aleatória em suas respostas, para evitar padrões previsíveis."},
            {"role": "system", "content": 'Use o formato: {"questionario":[{"enunciado":"Enunciado da pergunta?","alternativas":{"a":"Alternativa A","b":"Alternativa B","c":"Alternativa C","d":"Alternativa D"},"resposta":"a"}]}.'},
            {"role": "system", "content": "Responda apenas no formato JSON, sem comentários pessoais. Seja sucinto nas alternativas, evitando repetir o enunciado na resposta."},
            {"role": "system", "content": "Cada pergunta deve ter apenas uma resposta correta."},
            {"role": "system", "content": "Certifique-se de que as alternativas fornecidas permitam que a pergunta seja respondida de maneira adequada e direta, sem depender de informações externas."},
            {"role": "system", "content": "Não responda como chat, apenas devolva o modelo. Use sempre o formato JSON especificado para todas as respostas geradas pelo GPT."},
            {"role": "system", "content": "Se não for especificada a quantidade de questões ou enunciados, o padrão será exclusivamente 1 (uma) questão."},
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
