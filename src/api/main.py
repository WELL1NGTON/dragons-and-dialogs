import os
import openai
from fastapi import FastAPI

from Models.Resposta import Resposta
from Models.Pergunta import Pergunta

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/chat-gpt-test")
async def chat_gpt_test(Pergunta: str):
    messages = [ {"role": "system", "content": "Você é um mestre de D&D 3.5, e você está mestrando uma aventura, aujude o usuário"} ]
    # message = input("User : ")
    message = Pergunta
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
    reply = chat.choices[0].message.content
    # print(f"ChatGPT: {reply}")
    # messages.append({"role": "assistant", "content": reply})
    
    return {
        "resposta": reply
    }