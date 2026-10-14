# API Fila de Atendimento

Projeto desenvolvido para a disciplina de Desenvolvimento de APIs e Microsserviços utilizando FastAPI.

## Objetivo

Implementar uma API para gerenciamento de fila de atendimento presencial.

## Tecnologias Utilizadas

- Python
- FastAPI
- Uvicorn
- Pydantic

## Funcionalidades

### GET /fila
Lista todos os clientes não atendidos.

### GET /fila/{id}
Busca um cliente pela posição na fila.

### POST /fila
Adiciona um novo cliente à fila.

### PUT /fila
Atualiza a fila após um atendimento.

### DELETE /fila/{id}
Remove um cliente da fila.

## Requisitos Bônus

- Sistema de prioridade (N e P)

## Como Executar

### Instalar dependências

```bash
pip install -r requirements.txt