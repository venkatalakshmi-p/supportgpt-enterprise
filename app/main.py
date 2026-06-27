from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, chat
from app.rag.ingest import ingest_documents

app = FastAPI(title="SupportGPT Enterprise")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    ingest_documents()

app.include_router(auth.router)
app.include_router(chat.router)

@app.get("/")
def read_root():
    return {"message": "SupportGPT Enterprise Backend is running!"}