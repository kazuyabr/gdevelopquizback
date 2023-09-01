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

@router.get("/")
async def get_questionario():
    return { "message" : "Sou questionario!" }

@router.post("/")
async def questionario(prompt: Prompt):
     
    print(prompt.msg)   
     
    questionariogpt = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você deve elaborar questionarios com base no tema escolhido pelo usuario!"},
            {"role": "system", "content": "O tema sera composto apenas de uma unica palavra e a partir dela você formula o questionario se baseando em todas as regras aqui estabelecidas"},
            {"role": "system", "content": "Os questionarios precisam ser compostos por 1 enunciado, 4 alternativas de A, B, C, e D"},
            {"role": "system", "content": "O resultado a ser entregue para o usuario deve ser sempre composto de um JSON no formato enunciado, alternativas e resposta. Sendo resposta a letra da alternativa correta listada neste json!"},
            {"role": "system", "content": "Responda apenas no formato de json a seguir e seja direto, não quero comentario, não quero respostas de uma pessoa. quero apenas o retorno em JSON"},
            {"role": "system", "content": "seja sucinto ao definir as alternativas e não repita a pergunta nas alternativas, mas sim com possiveis respostas diretas!"},
            {"role": "system", "content": "importantissimo, só pode ter uma resposta correta!"},
            {"role": "system", "content": "importantissimo, a letra da alternativa deve variar de forma aleatória!"},
            {"role": "system", "content": 'Não importa o tema escolhido, sempre retorn o formato de json exemplificado a seguir: {"questionario":{		"alternativas": {			"a": "Com certeza é uma pergunta de teste",			"b": "Talvez seja uma pergunta de teste",			"c": "Não é uma pergunta de teste",			"d": "Nenhuma das anteriores"		},		"enunciado": "Pergunta de teste?",		"resposta": "a"	}}'},
            {"role": "user", "content": prompt.msg},
        ]
    )
    
    result = questionariogpt.choices[0].message.content
    result_json = json.loads(result)
    
    return { "response" : result_json }

@router.get("/{id}")
async def get_questionario(id: int):
    multi = id**2
    return { "message" : multi }
