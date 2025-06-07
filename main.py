from fastapi import FastAPI, APIRouter, HTTPException, Path
from typing import List, Dict
import sqlite3

app = FastAPI()
router = APIRouter()

# Tabelas válidas
TABELAS_VALIDAS = {"producao", "comercializacao", "exportacao", "importacao", "processamento"}

# Função de conexão
def get_connection():
    return sqlite3.connect("vitibrasil.db", check_same_thread=False)

# ----------------------------
# ROTA 1 – Consulta por ANO
# ----------------------------
@router.get(
    "/{tabela}/{ano}",
    summary="Consulta dados por tabela e ano",
    description="""
Consulta os dados de uma tabela específica para um ano informado.

**Tabelas válidas:**
- `producao`
- `comercializacao`
- `exportacao`
- `importacao`
- `processamento`
""",
    response_description="Lista de registros encontrados no banco de dados"
)
def listar_por_ano(
    tabela: str = Path(..., description="Nome da tabela (ex: producao, exportacao, processamento, comercializacao, importacao)"),
    ano: int = Path(..., ge=1970, le=2024, description="Ano dos dados (de 1970 a 2024)")
) -> Dict[str, List[Dict]]:
    tabela = tabela.lower()
    if tabela not in TABELAS_VALIDAS:
        raise HTTPException(status_code=400, detail="Tabela não suportada para consulta.")

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        if tabela in ("producao", "comercializacao"):
            query = f'SELECT ano, produto, quantidade_l FROM "{tabela}" WHERE ano = ?'
        elif tabela in ("exportacao", "importacao"):
            query = f'SELECT ano, "países", quantidade_kg, "valor_us$" FROM "{tabela}" WHERE ano = ?'
        elif tabela == "processamento":
            query = f'SELECT ano, cultivar, quantidade_kg, "sem_definição" FROM "{tabela}" WHERE ano = ?'

        cursor.execute(query, (ano,))
        resultados = [dict(row) for row in cursor.fetchall()]
        return {tabela: resultados}

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {e}")
    finally:
        conn.close()

# ----------------------------
# ROTA 2 – Consulta COMPLETA
# ----------------------------
TABELAS_VALIDAS = ("producao", "comercializacao", "exportacao", "importacao", "processamento")

def get_connection():
    return sqlite3.connect("vitibrasil.db", check_same_thread=False)

# ✅ ROTA: Retorna todos os registros da tabela informada
@router.get(
    "/{tabela}",
    summary="Retorna a tabela completa",
    description="Retorna todos os registros da tabela especificada, sem filtrar por ano.",
    response_description="Todos os dados da tabela em formato JSON"
)
def listar_tabela_completa(
    tabela: str = Path(..., description="Nome da tabela (ex: producao, exportacao, importacao, processamento)")
) -> Dict[str, List[Dict]]:
    tabela = tabela.lower()
    if tabela not in TABELAS_VALIDAS:
        raise HTTPException(status_code=400, detail=f"Tabela '{tabela}' não é suportada.")

    conn = get_connection()
    conn.row_factory = sqlite3.Row  # Permite acessar por nome da coluna
    cursor = conn.cursor()

    try:
        cursor.execute(f'SELECT * FROM "{tabela}"')
        registros = [dict(row) for row in cursor.fetchall()]
        return {tabela: registros}
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Erro ao acessar o banco: {e}")
    finally:
        conn.close()

# 🔽 Inclui o router na aplicação
app.include_router(router)
