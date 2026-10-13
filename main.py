from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime

app = FastAPI(
    title="API Fila de Atendimento",
    description="Projeto da disciplina de Desenvolvimento de APIs e Microsserviços",
    version="2.0"
)

fila = []

class Cliente(BaseModel):
    nome: str = Field(..., max_length=20)
    tipo: str = Field(..., min_length=1, max_length=1)

@app.get("/")
def home():
    return {"mensagem": "API funcionando!"}


@app.get("/fila")
def listar_fila():
    return [
        {
            "posicao": cliente["posicao"],
            "nome": cliente["nome"],
            "data_chegada": cliente["data_chegada"]
        }
        for cliente in fila
        if cliente["atendido"] == False
    ]

@app.get("/fila/{id}")
def buscar_cliente(id: int):

    for cliente in fila:
        if cliente["posicao"] == id and cliente["atendido"] == False:
            return {
                "posicao": cliente["posicao"],
                "nome": cliente["nome"],
                "data_chegada": cliente["data_chegada"]
            }

    raise HTTPException(
        status_code=404,
        detail="Cliente não encontrado."
    )

@app.post("/fila")
def adicionar_cliente(cliente: Cliente):

    if cliente.tipo not in ["N", "P"]:
        raise HTTPException(
            status_code=400,
            detail="O tipo deve ser N ou P."
        )

    novo_cliente = {
        "posicao": len(fila) + 1,
        "nome": cliente.nome,
        "tipo": cliente.tipo,
        "data_chegada": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "atendido": False
    }

    fila.append(novo_cliente)

    return novo_cliente