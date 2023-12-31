import json
import os
import unicodedata

import openai
from dotenv import load_dotenv
from fastapi import APIRouter

load_dotenv()

openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_KEY")


router = APIRouter(
    prefix="/forca",
    tags=["forca"],
    responses={404: {"description": "Not found"}}
)


# Função para remover acentos e caracteres especiais
def normalizar(texto):
    # Normalizar para o formato NFC (Forma Normalizada de Composição)
    texto_normalizado = unicodedata.normalize('NFKD', texto)
    #Remove espaços
    texto_normalizado = ''.join(c for c in texto_normalizado if unicodedata.category(c) != 'Mn' and c.isalnum())
    return texto_normalizado.encode('ASCII', 'ignore').decode('utf-8')

@router.get("/")
async def forca():
    
    max_attempts = 3  # Número máximo de tentativas
    attempt = 0
    
    while attempt < max_attempts:
        try:
        
            forca = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Elabore uma palavra e uma dica curta para o jogo forca."},
                    {"role": "system", "content": "Responda apenas no formato JSON, sem comentários pessoais. Seja sucinto nas alternativas, evitando repetir o enunciado na resposta."},
                    {"role": "system", "content": "As palavras devem sempre estar em maiusculas e sem sempre uma só palavra."},
                    {"role": "system", "content": "A dica não pode entregar a palavra diretamente afinal é para ser uma dica e não uma resposta."},
                    {"role": "system", "content": "A dica no final deve mencionar a quantidade de letras da palavra. Exemplo: Astro rei com 3 letras."},
                    {"role": "system", "content": "Seja direto."},
                    {"role": "system", "content": "Seja mais variado em elaborar a dica e a palavra."},
                    {"role": "system", "content": "Seja ambrangente e use temas amplos, não fique retornando só dados do formato como naruto, hokage, ninja, seja mais variado retornado por exemplo um personagem de filme séries ciencia"},
                    {"role": "system", "content": "Respeite sempre o formato {'dica': '', 'palavra': ['']} pois o que esta em branco pode variar"},
                    {"role": "system", "content": "A dica e a palavra precisam estar coerentes e dizer quantas letras a palavra tem."},
                    {"role": "system", "content": "Na palavra nunca use acentos nem caracteres especiais, nem numeros, só letras e caso haja letras com acentos como ç ou á por exemplo apenas tire o acento por exemplo ç se tornará c e á se tornará a."},
                    {"role": "system", "content": "É obrigatório colocar as letras da palavra cada um em uma posição do array sempre. exemplo: ['S', 'O', 'L']"},
                    {"role": "system", "content": "É obrigatorio a palavra não ter acentuações."},
                    {"role": "system", "content": "É obrigatorio manter coerencia entre dica e palavra."},
                    {"role": "system", "content": 'exemplo errado: {"dica": "Esporte coletivo", "palavra": "Futebol"}'},
                    {"role": "system", "content": 'exemplo correto: {"dica": "Esporte coletivo", "palavra": ["F", "U", "T", "E", "B", "O","L"]}'},
                    {"role": "system", "content": 'exemplo errado: {"dica":"Animal da selva","palavra":["L","E","O"]} o que está errado aqui é que foi omitido a letra Ã por conta do acento, mas o certo é exibir a letra sem acento ou seja A'},
                    {"role": "system", "content": 'exemplo correto: {"dica":"Animal da selva","palavra":["L","E", "A","O"]}'},
                    {"role": "system", "content": "Diversifique."}
                ]
            )
            
            forca = forca.choices[0].message.content
            result = json.loads(forca)
            result["palavra"] = [normalizar(string) for string in result["palavra"]]
            
            print(result)
            
            return result
        except openai.APIError as e:
                    attempt += 1
                    print(f"Tentativa {attempt} falhou. Motivo: {e}")
    
    return {"error": "Falha ao se comunicar com a OpenAI após várias tentativas."}

