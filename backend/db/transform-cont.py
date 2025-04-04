import os
import zipfile
import pandas as pd
from io import BytesIO

def processar_demonstracoes():
    base_path = os.path.join("backend", "db", "dados_ans")
    current_year = pd.Timestamp.now().year
    dados_consolidados = []
    
    output_dir = os.path.join(base_path, "processed")
    os.makedirs(output_dir, exist_ok=True)
    
    for ano in range(current_year - 2, current_year + 1):
        ano_path = os.path.join(base_path, str(ano))
        if not os.path.exists(ano_path):
            print(f"Pasta do ano {ano} não encontrada: {ano_path}")
            continue
            
        for trimestre in range(1, 5):
            zip_file = os.path.join(ano_path, f"{trimestre}T{ano}.zip")
            if not os.path.exists(zip_file):
                print(f"Arquivo não encontrado: {trimestre}T{ano}.zip")
                continue
                
            print(f"\nProcessando: {zip_file}")
            
            try:
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    for file_info in zip_ref.infolist():
                        if file_info.filename.lower().endswith('.csv'):
                            print(f"Extraindo dados de: {file_info.filename}")
                            with zip_ref.open(file_info) as csv_file:
                                df = pd.read_csv(csv_file, encoding='latin1', sep=';', decimal=',', thousands='.')
                                df['ano'] = ano
                                df['trimestre'] = f"T{trimestre}"
                                dados_consolidados.append(df)
            except Exception as e:
                print(f"Erro ao processar {zip_file}: {str(e)}")
                continue
    
    if dados_consolidados:
        df_final = pd.concat(dados_consolidados, ignore_index=True)
        df_final = clean_data(df_final)
        
        csv_final = os.path.join(output_dir, "demonstracoes_contabeis.csv")
        df_final.to_csv(csv_final, index=False, encoding='utf-8')
        print(f"\nDados consolidados salvos em: {csv_final}")
        print(f"Total de registros: {len(df_final)}")
    else:
        print("Nenhum dado foi processado. Verifique os arquivos de entrada.")

def clean_data(df):
    """Função para limpeza e padronização dos dados"""
    df = df.dropna(how='all', axis=1)
    
    if 'VL_SALDO_FINAL' in df.columns:
        df['valor'] = pd.to_numeric(df['VL_SALDO_FINAL'].astype(str).str.replace('.', '').str.replace(',', '.'), errors='coerce')
    elif 'valor' in df.columns:
        df['valor'] = pd.to_numeric(df['valor'].astype(str).str.replace('.', '').str.replace(',', '.'), errors='coerce')
    
    df.columns = df.columns.str.lower()
    
    return df

if __name__ == "__main__":
    print("Iniciando processamento de demonstrações contábeis...")
    processar_demonstracoes()