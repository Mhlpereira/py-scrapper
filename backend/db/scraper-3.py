import requests
import os
from datetime import datetime

def download_ans_data():
    base_dir = os.path.join("backend", "db", "dados_ans")
    os.makedirs(base_dir, exist_ok=True)

    operadoras_url = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"
    operadoras_path = os.path.join(base_dir, "operadoras_ativas.csv")
    
    with requests.get(operadoras_url, stream=True) as r:
        r.raise_for_status()
        with open(operadoras_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
 

    base_url = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
    current_year = datetime.now().year
    
    for ano in range(current_year - 2, current_year + 1):
        for bimestre in range(1, 5):  
            arquivo = f"{bimestre}T{ano}.zip"
            arquivo_url = f"{base_url}{ano}/{arquivo}"
            
            try:
                response = requests.head(arquivo_url)
                if response.status_code == 200:
                    ano_path = os.path.join(base_dir, str(ano))  # Corrigido aqui
                    os.makedirs(ano_path, exist_ok=True)
                    
                    with requests.get(arquivo_url, stream=True) as r:
                        r.raise_for_status()
                        output_path = os.path.join(ano_path, arquivo)
                        with open(output_path, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=8192):
                                f.write(chunk)
                    print(f"Baixado: {output_path}")
                else:
                    print()
                    
            except requests.exceptions.RequestException as e:
                print(f"🚨 Erro ao acessar {arquivo_url}: {str(e)}")

if __name__ == "__main__":
    download_ans_data()