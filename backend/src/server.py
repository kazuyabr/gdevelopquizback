from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.chat import router as chat_router
from src.routes.forca import router as forca_router
from src.routes.historiadinamica import router as historiadinamica_router
from src.routes.questionario import router as questionario_router

app = FastAPI()

# CORS
# origins = [
#     'http://localhost/',
#     ]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Rota para a raiz do projeto que seria algo como http://localhost/
@app.get("/", description="health check")
async def root():
    return {"message" : "check!"}

app.include_router(chat_router)
app.include_router(questionario_router)
app.include_router(historiadinamica_router)
app.include_router(forca_router)