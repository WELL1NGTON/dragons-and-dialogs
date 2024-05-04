import os
from datetime import datetime, timedelta, timezone

import openai
from db import add_user, get_user, verify_password
from fastapi import FastAPI, HTTPException, status
from jose import jwt
from Models.models import Token
from pony.orm import *

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


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


ACCESS_TOKEN_EXPIRE_HOURS = 24


@app.post('/login')
async def login(login: str, password: str):
    user = verify_password(login, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            deatils='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    access_token = create_access_token(
        data={'sub': user.login}, expires_delta=access_token_expires
    )
    # return {"login": user.login, "password": user.password_hash}
    return Token(access_token=access_token, token_type='bearer')
