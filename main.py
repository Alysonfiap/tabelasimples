from fastapi import FastAPI
from fastapi import Depends,HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import sqlite3
from fastapi import APIRouter, HTTPException
app = FastAPI(
    title = "My Fast API",
    version="1.0.0",
    description = "API de Exemplo Com FastAPI"
)
def get_connection():
    conn = sqlite3.connect("vitibrasil.db")
    conn.row_factory = sqlite3.Row  # permite acessar colunas por nome
    return conn
router = APIRouter()
@router.get("/{tabela}/{ano}")
def listar_produtos(tabela: str,ano: int):
    conn = get_connection()
    cursor = conn.cursor()
    if tabela.startswith(("ex", "impor")):
        cursor.execute(f"SELECT País, `{ano}` FROM `{tabela}`")
    elif tabela.startswith(("co", "pr")):
        cursor.execute(f"SELECT produto, `{ano}` FROM `{tabela}`")
    else:
        conn.close()
        raise HTTPException(status_code=400, detail="Tabela não suportada para consulta.")
    resultados = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {tabela: resultados}
app.include_router(router)
