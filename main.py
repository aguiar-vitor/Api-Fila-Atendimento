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
        "posicao": 0,
        "nome": cliente.nome,
        "tipo": cliente.tipo,
        "data_chegada": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "atendido": False
    }

    if cliente.tipo == "P":
        indice = 0

        while indice < len(fila) and fila[indice]["tipo"] == "P":
            indice += 1

        fila.insert(indice, novo_cliente)

    else:
        fila.append(novo_cliente)

    for i, pessoa in enumerate(fila, start=1):
        pessoa["posicao"] = i

    return novo_cliente

@app.put("/fila")
def atender_cliente():

    for cliente in fila:
        if cliente["posicao"] == 1:
            cliente["posicao"] = 0
            cliente["atendido"] = True
        elif not cliente["atendido"]:
            cliente["posicao"] -= 1

    return {"mensagem": "Fila atualizada com sucesso."}

@app.delete("/fila/{id}")
def remover_cliente(id: int):

    for cliente in fila:

        if cliente["posicao"] == id and not cliente["atendido"]:

            fila.remove(cliente)

            for i, pessoa in enumerate(
                [c for c in fila if not c["atendido"]],
                start=1
            ):
                pessoa["posicao"] = i

            return {
                "mensagem": f"Cliente da posição {id} removido com sucesso."
            }

    raise HTTPException(
        status_code=404,
        detail="Cliente não encontrado."
    )