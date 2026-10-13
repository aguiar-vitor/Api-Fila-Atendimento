from fastapi import FastAPI

app = FastAPI(
    title="API Fila de Atendimento",
    description="Projeto da disciplina de Desenvolvimento de APIs e Microsserviços",
    version="1.0"
)

@app.get("/")
def home():
    return {"mensagem": "API funcionando!"}