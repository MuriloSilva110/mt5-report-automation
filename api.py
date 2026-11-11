from fastapi import status
from fastapi import FastAPI, HTTPException
from main import carregar_configuracao
import json
from pathlib import Path


app = FastAPI()

@app.get("/")
def reed_root():
    return {
        "status": "online", 
    "projeto": "MT5 Report Automation"}

@app.get("/terminals")
def lista_terminais():
    return carregar_configuracao()

@app.get("/metricas/{nome_terminal}")
def obter_metricas(nome_terminal:str):
    caminho_arquivo = Path("relatorios") / f"metricas_consolidadas_{nome_terminal}.json"

    if not caminho_arquivo.exists():
        raise HTTPException(status_code=404, detail=f"Métricas não encontradas para o terminal '{nome_terminal}'")
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
        return dados


