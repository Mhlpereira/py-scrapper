from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
)

base_path = os.path.join("backend", "db", "dados_ans")
operadoras_csv = os.path.join(base_path, "operadoras_ativas.csv")

try:
    df_operadoras = pd.read_csv(
        operadoras_csv,
        sep=";",
        encoding='latin1',
        on_bad_lines='skip',
        dtype=str 
    )
    df_operadoras.columns = df_operadoras.columns.str.lower().str.replace(" ", "_")
except Exception as e:
    print(f"Erro ao carregar CSV: {e}")
    df_operadoras = pd.DataFrame()

@app.get("/api/operadoras/search")
async def buscar_operadoras(q: str = Query(None, min_length=2)):
    if df_operadoras.empty:
        raise HTTPException(status_code=500, detail="Dados não carregados")
    
    try:
        termo = q.lower()
        mask = (
            df_operadoras["razao_social"].str.lower().str.contains(termo, na=False) |
            df_operadoras["nome_fantasia"].str.lower().str.contains(termo, na=False) |
            df_operadoras["cidade"].str.lower().str.contains(termo, na=False) |
            df_operadoras["uf"].str.lower().str.contains(termo, na=False)
        )
        
        resultados = df_operadoras[mask].head(50)
        resultados = resultados.replace({np.nan: None})  # Converte NaN para None
        
        return {"results": resultados.to_dict(orient="records")}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro na busca: {str(e)}")