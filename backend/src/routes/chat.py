import os

import openai
from dotenv import load_dotenv
from fastapi import APIRouter
from pydantic import BaseModel

load_dotenv()

openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_KEY")

class Prompt(BaseModel):
    msg: str

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={404: {"description": "Not found"}}
)

@router.post("/")
async def chat(prompt: Prompt):
     
    print(prompt.msg)   
    max_attempts = 3  # Número máximo de tentativas
    attempt = 0
    
    while attempt < max_attempts:
        try:
        
            chatgpt = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um assistente do projeto QUIZ do canal Jogatinando!"},
                    {"role": "user", "content": prompt.msg},
                ]
            )
            
            result = chatgpt.choices[0].message.content
            
            return { "response" : result }
        except openai.APIError as e:
                    attempt += 1
                    print(f"Tentativa {attempt} falhou. Motivo: {e}")
    
    return {"error": "Falha ao se comunicar com a OpenAI após várias tentativas."}
