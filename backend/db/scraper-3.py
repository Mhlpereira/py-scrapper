import requests
import os
from datetime import datetime

def download_ans_data():
    os.makedirs("dados_ans", exist_ok=True)

    operadoras_url = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"
    operadoras_path = os.path.join("dados_ans", "operadoras_ativas.csv")
    
    with requests.get(operadoras_url, stream=True) as r:
        r.raise_for_status()
        with open(operadoras_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): # Lê o arquivo em partes
                f.write(chunk)
    print(f"Downloaded: {operadoras_path}")

    base_url = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
    current_year = datetime.now().year
    
    for ano in range(current_year - 2, current_year + 1):
        ano_url = f"{base_url}{ano}/"
        ano_path = os.path.join("dados_ans", str(ano))
        os.makedirs(ano_path, exist_ok=True)
        
        exemplo_arquivo = f"Demonstrações_Contábeis_{ano}.zip"
        with requests.get(f"{ano_url}{exemplo_arquivo}", stream=True) as r:
            if r.status_code == 200:
                with open(os.path.join(ano_path, exemplo_arquivo), 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Downloaded: {ano_path}/{exemplo_arquivo}")

if __name__ == "__main__":
    download_ans_data()