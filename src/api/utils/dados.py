from random import randint
from pydantic import BaseModel


class InputRolagem(BaseModel):
    tipo: str
    quantidade: int


class OutputRolagem(BaseModel):
    tipo: str
    resultado: int


class ResultadoRolagens(BaseModel):
    resultados: list[OutputRolagem]
    total: int


def rolar_dados(input: list[InputRolagem]) -> ResultadoRolagens:
    dados_rolados = ResultadoRolagens(resultados=[], total=0)
    for item in input:
        for _ in range(0, item.quantidade):
            faces = int(item.tipo[1:])
            resultado = randint(1, faces)
            dados_rolados.total += resultado
            dados_rolados.resultados.append(
                OutputRolagem(tipo=item.tipo, resultado=resultado)
            )
    return dados_rolados
