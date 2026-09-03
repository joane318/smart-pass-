from fastapi import FastAPI

app = FastAPI(
    title="API de Saídas Escolares",
    description="API para o sistema de registro de saídas antecipadas",
    version="1.0"
)


@app.get("/")
def inicio():
    return {
        "mensagem": "API de Saídas Escolares funcionando!"
    }