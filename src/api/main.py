import json
import os
from datetime import datetime as dt

import openai
import psycopg2
from fastapi import FastAPI
from Models.Pergunta import Pergunta
from Models.Resposta import Resposta
from pony.orm import *

from db import add_user, get_user, login_user

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/chat-gpt-test")
async def chat_gpt_test(Pergunta: str):
    messages = [
        {
            "role": "system",
            "content": "Você é um mestre de D&D 3.5, e você está mestrando uma aventura, ajude o usuário",
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


@app.post('/users')
async def create_user(login: str, password: str):
    add_user(login=login, password=password)
    return {"message": " Usuário adicionado com sucesso!"}


@app.get('/users/{id}')
async def get_by_id(id: int):
    user = get_user(id)
    return {"login": user.login, "id": user.id}


@app.post('/login')
async def login(login: str, password: str):
    user = login_user(login, password)
    return {"login": user.login, "password": user.password_hash}
