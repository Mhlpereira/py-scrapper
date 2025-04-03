import pdfplumber
import pandas as pd
import zipfile
import os

def transform_data(anexo_i_path):
    name = "mario_henrique_lino_pereira"

    rol_tables = []

    with pdfplumber.open(anexo_i_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table() 
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])  
                if "OD" in df.columns and "AMB" in df.columns:
                    rol_tables.append(df)

    if rol_tables:
        combined_table = pd.concat(rol_tables, ignore_index=True)

        od_mapping = {
            "Seg": "Segmentação",
            "Amb": "Ambulatorial",
            "Hosp": "Hospitalar",
            "AMB": "Ambulatorial",
            "HOS": "Hospitalar",
        }

        amb_mapping = {
            "Sim": "Procedimento ambulatorial",
            "Não": "Procedimento não ambulatorial",
            "S": "Procedimento ambulatorial",
            "N": "Procedimento não ambulatorial",
        }

        for col, mapping in [("OD", od_mapping), ("AMB", amb_mapping)]:
            if col in combined_table.columns:
                combined_table[col] = combined_table[col].map(mapping).fillna(combined_table[col])

        csv_filename = "rol_procedimentos.csv"
        combined_table.to_csv(csv_filename, index=False, encoding="utf-8")

        zip_filename = f"Teste_{name}.zip"
        with zipfile.ZipFile(zip_filename, "w") as zipf:
            zipf.write(csv_filename)

        print(f"Data extraída e salva em {csv_filename}")
        print(f"CSV compactado em {zip_filename}")

        return zip_filename
    else:
        print("Nenhuma tabela encontrada no PDF")
        return None


if __name__ == "__main__":
    with zipfile.ZipFile("anexos.zip", "r") as zip_ref:
        zip_ref.extractall("extracted")

    anexo_i_path = None
    for file in os.listdir("extracted"):
        if "Anexo_I" in file and file.endswith(".pdf"):
            anexo_i_path = os.path.join("extracted", file)
            break

    if anexo_i_path:
        transform_data(anexo_i_path)
    else:
        print("Anexo I não encontrado nos arquivos extraídos")
