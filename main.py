from fastapi import FastAPI, APIRouter, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from typing import List, Dict

app = FastAPI(
    title="API Vitibrasil",
    version="1.0.0",
    description="Consulta dados da produção, comercialização, exportação, importação e processamento de uvas e vinhos no Brasil, extraídos da Embrapa (Vitibrasil)."
)

# Configuração CORS para liberar chamadas externas
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_connection():
    conn = sqlite3.connect("vitibrasil.db")
    conn.row_factory = sqlite3.Row
    return conn

router = APIRouter(prefix="/api")

# Lista segura de tabelas permitidas para consulta
TABELAS_VALIDAS = [
    "producao",
    "comercializacao",
    "exportacao",
    "importacao",
    "processamento"
]

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
def listar_produtos(
    tabela: str = Path(..., description="Nome da tabela (ex: producao, exportacao, processamento)"),
    ano: int = Path(..., ge=1970, le=2024, description="Ano dos dados (de 1970 a 2024)")
) -> Dict[str, List[Dict]]:
    # Verifica se a tabela é válida
    tabela = tabela.lower()
    if tabela not in TABELAS_VALIDAS:
        raise HTTPException(status_code=400, detail="Tabela não suportada para consulta.")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Monta a query conforme a tabela (colunas exatas)
        if tabela in ("producao", "comercializacao"):
            query = f'SELECT ano, produto, quantidade_l FROM "{tabela}" WHERE ano = ?'
        elif tabela in ("exportacao", "importacao"):
            # Note que nomes de colunas com acento e símbolo precisam de aspas duplas no SQLite
            query = f'SELECT ano, "países", quantidade_kg, "valor_us$" FROM "{tabela}" WHERE ano = ?'
        elif tabela == "processamento":
            query = f'SELECT ano, cultivar, quantidade_kg, "sem_definição" FROM "{tabela}" WHERE ano = ?'
        else:
            # Isso não deve acontecer porque validamos antes, mas só por segurança
            raise HTTPException(status_code=400, detail="Tabela inválida.")

        cursor.execute(query, (ano,))
        resultados = [dict(row) for row in cursor.fetchall()]
        return {tabela: resultados}

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {e}")
    
    finally:
        conn.close()

app.include_router(router)
