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
    prefix="/historiadinamica",
    tags=["historiadinamica"],
    responses={404: {"description": "Not found"}}
)


@router.post("/")
async def historiadinamica(prompt: Prompt):
     
    print(prompt.msg)   
        
    if prompt.msg in ["", 0]:
        user_msg = "Comece uma história e só escreva o seu primeiro paragrafo!"
    else:
        user_msg = prompt.msg
        
    
    historiadinamicagpt = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
           {"role": "system", "content": "Continue a história de forma direta e sem adicionar diálogos."},

            {"role": "system", "content": 'Quando a mensagem enviada contiver texto superior a 5 palavras interprete como história que deve ser continuada a partir do fim desta mensagem'},

            {"role": "system", "content": 'Enterprete o texto que sera continuado para que a continuação de mais sentido ao estilo de história que esta sendo contada com base no tipo dela (ação, aventura, drama, comédia, terror ...)'},

            {"role": "system", "content": 'Gere apenas um paragrafo.'},
            
            {"role": "user", "content": user_msg}
            
        ]
    )
    
    paragrafo = historiadinamicagpt.choices[0].message.content
    
    destacarfrases = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Encontre pelo menos duas palavras ou mais no texto que se forem mudadas, afetariam todo o contexto da história e destaque-as usando # no inicio e no fim da palavra para ficar facilmente visivel no paragrafo! (exemplo: #palavraasermudada#"},
            {"role": "system", "content": "O isolamento deve ocorrer dentro da história sem qualquer alteração a não ser a adição dos #. (exemplo: Era uma vez joaninha que #sentiu# muito #frio#) neste exemplo o texto sera copiado e atualizado pelo usuario e reenviado de novo mas de maneira conveniente sem mudar o texto completo apenas as palavras destacadas!"},
            {"role": "user", "content": paragrafo}
            
        ]
    )
    
    result = destacarfrases.choices[0].message.content
    
    return {"result" : result}
    # result_json = json.loads(result)
    
    # return { "response" : result_json }


@router.get("/{id}")
async def get_historiadinamica(id: int):
    multi = id ** 2
    return { "message": multi }
