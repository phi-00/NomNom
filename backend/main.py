from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  # importante por causa do Authorization
)


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import get_settings
from routers import auth, ingredientes, receitas, lista_compras, utilizador

# Importar outros routers aqui quando criar
# from routers import example

settings = get_settings()

app = FastAPI(
    title="NomNom API",
    description="API para conectar o frontend com Supabase",
    version="1.0.0",
    debug=settings.debug
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "Bem-vindo à NomNom API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Verifica o status da API"""
    return {"status": "healthy"}


# Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Autenticação"])
app.include_router(utilizador.router, prefix="/api/v1/utilizador", tags=["Utilizador"])
app.include_router(ingredientes.router, prefix="/api/v1/ingredientes", tags=["Ingredientes"])
app.include_router(receitas.router, prefix="/api/v1/receitas", tags=["Receitas"])
app.include_router(lista_compras.router, prefix="/api/v1/lista-compras", tags=["Lista de Compras"])

# Incluir outros routers aqui quando criar
# app.include_router(example.router, prefix="/api/v1", tags=["example"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
