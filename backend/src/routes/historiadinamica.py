from typing import List
from fastapi import APIRouter
from dotenv import load_dotenv
from pydantic import BaseModel
import openai
import os
import json
import array

load_dotenv()

openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_KEY")


class Prompt(BaseModel):
    msg: str
    replace: List[str]


router = APIRouter(
    prefix="/historiadinamica",
    tags=["historiadinamica"],
    responses={404: {"description": "Not found"}}
)


@router.post("/")
async def historiadinamica():
    max_attempts = 3  # Número máximo de tentativas
    attempt = 0
    
    while attempt < max_attempts:
        try:
    
            historiadinamicagpt = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Conte a história de forma direta e sem adicionar diálogos."},

                    {"role": "system", "content": 'Quando a mensagem enviada contiver texto superior a 5 palavras interprete como história que deve ser continuada a partir do fim desta mensagem'},

                    {"role": "system", "content": 'Enterprete o texto que sera continuado para que a continuação de mais sentido ao estilo de história que esta sendo contada com base no tipo dela (ação, aventura, drama, comédia, terror ...)'},

                    {"role": "system", "content": 'Gere apenas um paragrafo de no maximo 5 linhas.'},
                    
                    {"role": "user", "content": "Comece uma história e só escreva o seu primeiro paragrafo!"}
                    
                ]
            )
            
            paragrafo = historiadinamicagpt.choices[0].message.content
            
            destacarfrases = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Encontre no minimo duas a no maximo seis palavras no texto que se forem mudadas, afetariam todo o contexto da história e destaque-as usando a tag [b][color=#F54747][/color][/b] no inicio e no fim da palavra para ficar facilmente visivel no paragrafo! (exemplo: [b][color=#F54747]palavraasermudada[/color][/b]"},
                    {"role": "system", "content": "Não omita o texto original"},
                    {"role": "system", "content": "O isolamento deve ocorrer dentro do texto sem qualquer alteração a não ser a adição dos [b] e [color]. (modelo a ser seguido: Era uma vez joaninha que [b][color=#F54747]sentiu[/color][/b] muito [b][color=#F54747]frio[/color][/b]) neste exemplo o texto sera copiado e atualizado pelo usuario e reenviado de novo mas de maneira conveniente sem mudar o texto completo apenas as palavras destacadas!"},
                    {"role": "user", "content": paragrafo}
                    
                ]
            )
    
            result = destacarfrases.choices[0].message.content
            
            return {"result": result}
        except openai.APIError as e:
            attempt += 1
            print(f"Tentativa {attempt} falhou. Motivo: {e}")
    
    return {"error": "Falha ao se comunicar com a OpenAI após várias tentativas."}


@router.post("/continue")
async def historiadinamica_continue(prompt: Prompt):
    modified_msg = prompt.msg

    for replacement in prompt.replace:
        if replacement.strip() and "," in replacement:
            words = replacement.split(',')
            if len(words) == 2:
                modified_msg = modified_msg.replace(words[0], words[1])

    print(modified_msg)
    
    max_attempts = 3  # Número máximo de tentativas
    attempt = 0
    
    while attempt < max_attempts:
        try:
    
            historiadinamicagpt = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Conte a história de forma direta e sem adicionar diálogos."},

                    {"role": "system", "content": 'Continue a história a partir de onde o texto parou.'},
                    
                    {"role": "system", "content": 'Enterprete o texto base e de um tom mais aprofundado para empolgar o leitor.'},

                    {"role": "system", "content": 'Gere apenas um paragrafo de no maximo 5 linhas.'},
                    
                    {"role": "user", "content": modified_msg}
                    
                ]
            )
            
            paragrafo = historiadinamicagpt.choices[0].message.content
            
            destacarfrases = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Encontre no minimo duas a no maximo seis palavras no texto que se forem mudadas, afetariam todo o contexto da história e destaque-as usando a tag [b][color=#F54747][/color][/b] no inicio e no fim da palavra para ficar facilmente visivel no paragrafo! (exemplo: [b][color=#F54747]palavraasermudada[/color][/b]"},
                    {"role": "system", "content": "Não omita o texto original"},
                    {"role": "system", "content": "O isolamento deve ocorrer dentro do texto sem qualquer alteração a não ser a adição dos [b] e [color]. (modelo a ser seguido: Era uma vez joaninha que [b][color=#F54747]sentiu[/color][/b] muito [b][color=#F54747]frio[/color][/b]) neste exemplo o texto sera copiado e atualizado pelo usuario e reenviado de novo mas de maneira conveniente sem mudar o texto completo apenas as palavras destacadas!"},
                    {"role": "user", "content": paragrafo}
                    
                ]
            )
    
            result = destacarfrases.choices[0].message.content
            
            return {"result": result}
        except openai.APIError as e:
            attempt += 1
            print(f"Tentativa {attempt} falhou. Motivo: {e}")
    
    return {"error": "Falha ao se comunicar com a OpenAI após várias tentativas."}
