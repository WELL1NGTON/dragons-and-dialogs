import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import openai
from db import add_user, get_user, verify_password, User
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from jose.exceptions import JWEInvalidAuth
from Models.models import Token, TokenData
from pony.orm import *
from utils.dados import InputRolagem, ResultadoRolagens, rolar_dados

SECRET_KEY = os.getenv('SECRET_KEY')  # your secret key here
ALGORITHM = 'HS256'  # Coding algorithm


# function who return a new token session everytime the old one expires
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
oauth2_scheme = HTTPBearer()


@app.post("/chat-gpt-test")
async def chat_gpt_test(Pergunta: str):
    messages = [
        {
            "role": "system",
            "content": "Você é um mestre de D&D 3.5, e você está mestrando uma aventura, ajude o usuário",
        }
    ]
    message = Pergunta
    if message:
        messages.append({"role": "user", "content": message})
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
    reply = chat.choices[0].message.content
    return {"resposta": reply}


@app.post('/users')
async def create_user(login: str, password: str):
    add_user(login=login, password=password)
    return {"message": " Usuário adicionado com sucesso!"}


@app.get('/users/{username}')
async def get_by_id(username: str):
    user = get_user(username)
    return {"login": user.login, "id": user.id}


ACCESS_TOKEN_EXPIRE_HOURS = 24


# This endpoint is used to authenticate a user with a login and password and generate a valid access token (JWT) for use in later authentication.
@app.post('/token')
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
    return Token(access_token=access_token, token_type='bearer')


async def get_current_user(
    token: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)]
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(
            token.credentials, SECRET_KEY, algorithms=[ALGORITHM]
        )
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWEInvalidAuth:
        raise credentials_exception
    user = get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user


# This endpoint is used to roll the dices using Input and result classes
@app.post('/dados')
async def dados(
    args: list[InputRolagem],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ResultadoRolagens:
    if len(args) > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Please use only 10 dices types at maximum, will you need all theses dices? o.o',
        )
    for item in args:
        if item.quantidade > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Please roll only 100 dices at a time, our serves will be thankfull :)',
            )

    return rolar_dados(args)
