import os
from datetime import datetime as dt

import openai
from fastapi import FastAPI
from Models.Pergunta import Pergunta
from Models.Resposta import Resposta
from peewee import *

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/gibe-sauce')
async def soyce():
    return {'message': 'gibe the soyce'}


@app.post("/chat-gpt-test")
async def chat_gpt_test(Pergunta: str):
    messages = [
        {
            "role": "system",
            "content": "Você é um mestre de D&D 3.5, e você está mestrando uma aventura, aujude o usuário",
        }
    ]
    # message = input("User : ")
    message = Pergunta
    if message:
        messages.append({"role": "user", "content": message})
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
    reply = chat.choices[0].message.content
    # print(f"ChatGPT: {reply}")
    # messages.append({"role": "assistant", "content": reply})

    return {"resposta": reply}


