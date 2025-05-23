from fastapi import FastAPI
from fastapi import Depends,HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
app = FastAPI(
    title = "My Fast API",
    version="1.0.0",
    description = "API de Exemplo Com FastAPI"
)
@app.get("/")
async def home():
    return "Hello, FastAPI"

import sqlite3

def get_connection():
    conn = sqlite3.connect("vitibrasil.db")
    conn.row_factory = sqlite3.Row  # permite acessar colunas por nome
    return conn

from fastapi import APIRouter, HTTPException
from database.db import get_connection

router = APIRouter()

@router.get("/produtos")
def listar_produtos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT Produto FROM comercio")
    produtos = [row["Produto"] for row in cursor.fetchall()]
    conn.close()
    return {"produtos": produtos}





