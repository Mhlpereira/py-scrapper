import tabula
import pandas as pd
import zipfile
import os


def transform_data(anexo_i_path):
    name = "mario_henrique_lino_pereira"

    tables = tabula.read_pdf(anexo_i_path, pages="all", multiple_tables=True)

    rol_tables = []
    for table in tables:
        if "OD" in table.columns and "AMB" in table.columns:
            rol_tables.append(table)

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
                combined_table[col] = (
                    combined_table[col].map(mapping).fillna(combined_table[col])
                )

        csv_filename = "rol_procedimentos.csv"
        combined_table.to_csv(csv_filename, index=False, encoding="utf-8")

        zip_filename = f"Teste_{name}.zip"
        with zipfile.ZipFile(zip_filename, "w") as zipf:
            zipf.write(csv_filename)

        print(f"Data extracted and saved to {csv_filename}")
        print(f"CSV compressed into {zip_filename}")

        return zip_filename
    else:
        print("Could not find the required table in the PDF")
        return None


if __name__ == "__main__":
    with zipfile.ZipFile("anexos.zip", "r") as zip_ref:
        zip_ref.extractall("extracted")

    anexo_i_path = None
    for file in os.listdir("extracted"):
        if "Anexo I" in file and file.endswith(".pdf"):
            anexo_i_path = os.path.join("extracted", file)
            break

    if anexo_i_path:
        transform_data(anexo_i_path, "name")
    else:
        print("Anexo I not found in the extracted files")
