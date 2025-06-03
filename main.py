from fastapi import FastAPI, APIRouter, HTTPException, Path
import sqlite3
from typing import List, Dict

app = FastAPI(
    title="API Vitibrasil",
    version="1.0.0",
    description="Consulta dados da produção, comercialização, exportação, importação e processamento de uvas e vinhos no Brasil, extraídos da Embrapa (Vitibrasil)."
)

def get_connection():
    conn = sqlite3.connect("vitibrasil.db")
    conn.row_factory = sqlite3.Row  # Retorna linhas como dicionários
    return conn

router = APIRouter()

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
    """
    Retorna os registros da tabela e ano especificados.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        if tabela.startswith(("producao", "comercializacao")):
            cursor.execute(f"SELECT ano, produto, quantidade_l FROM `{tabela}` WHERE ano = ?", (ano,))
        elif tabela.startswith(("exportacao", "importacao")):
            cursor.execute(f"SELECT ano, países, quantidade_kg, valor_us$ FROM `{tabela}` WHERE ano = ?", (ano,))
        elif tabela.startswith("processamento"):
            cursor.execute(f"SELECT ano, cultivar, quantidade_kg, sem_definição FROM `{tabela}` WHERE ano = ?", (ano,))
        else:
            raise HTTPException(status_code=400, detail="Tabela não suportada para consulta.")
        
        resultados = [dict(row) for row in cursor.fetchall()]
        return {tabela: resultados}

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {e}")
    
    finally:
        conn.close()

app.include_router(router)
