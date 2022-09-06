from fastapi import FastAPI
from router.user import user
from router.chamado import chamado
from router.problema import problemas
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user)
app.include_router(chamado)
app.include_router(problemas)