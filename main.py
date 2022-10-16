from fastapi import FastAPI
from router.user import user_router
from router.chamado import chamado_router
from router.problema import problemas_router
from router.acompanhamento import acompanhamentos_router
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

app.include_router(user_router)
app.include_router(chamado_router)
app.include_router(problemas_router)
app.include_router(acompanhamentos_router)
