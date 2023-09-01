from fastapi import APIRouter
from dotenv import load_dotenv
from pydantic import BaseModel
import openai
import os

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

@router.get("/")
async def get_chat():
    return { "message" : "Sou chat!" }

@router.post("/")
async def chat(prompt: Prompt):
     
    print(prompt.msg)   
     
    chatgpt = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente do projeto QUIZ do canal Jogatinando!"},
            {"role": "user", "content": prompt.msg},
        ]
    )
    
    result = chatgpt.choices[0].message.content
    
    return { "response" : result };

@router.get("/{id}")
async def get_chat(id: int):
    multi = id**2
    return { "message" : multi }
