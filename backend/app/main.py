from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
)

try:
    df_operadoras = pd.read_csv(
        "data/operadoras_ativas.csv",
        sep=";",
        encoding="latin1",
        on_bad_lines="skip"
    )
    df_operadoras.columns = df_operadoras.columns.str.lower().str.replace(" ", "_")
except Exception as e:
    print(f"Erro ao carregar CSV: {e}")
    df_operadoras = pd.DataFrame()

@app.get("/api/operadoras")
async def buscar_operadoras(termo: str = Query(None, min_length=2)):
    if df_operadoras.empty:
        raise HTTPException(status_code=500, detail="Dados não carregados")
    
    termo = termo.lower()
    resultados = df_operadoras[
        df_operadoras["razao_social"].str.lower().str.contains(termo, na=False)
    ].head(50) 
    
    return resultados.to_dict(orient="records")