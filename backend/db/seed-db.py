import psycopg2
import os

def execute_sql_file(conn, filename):
    try:
        with open(filename, 'r') as file:
            sql_script = file.read()
        cursor = conn.cursor()
        
        statements = sql_script.split(';')
        for statement in statements:
            if statement.strip():
                cursor.execute(statement)
        
        conn.commit()
        cursor.close()
        print(f"Successfully executed {filename}")
    except Exception as e:
        print(f"Erro ao executar {filename}: {e}")
        raise

def import_csv_file(conn, table_name, csv_file, columns, delimiter=';', encoding='LATIN1'):
    try:
        if not os.path.exists(csv_file):
            print(f"Error: File not found: {csv_file}")
            return False
        
        copy_sql = f"COPY {table_name} ({', '.join(columns)}) FROM STDIN WITH CSV DELIMITER '{delimiter}' HEADER ENCODING '{encoding}'"
        
        cursor = conn.cursor()
        with open(csv_file, 'r', encoding=encoding) as f:
            cursor.copy_expert(copy_sql, f)
        
        conn.commit()
        cursor.close()
        print(f"Successfully imported {csv_file} into {table_name}")
        return True
    except Exception as e:
        print(f"Error importing {csv_file}: {e}")
        conn.rollback()
        return False

if __name__ == "__main__":
    conn = psycopg2.connect(
        dbname="ans_database",
        user="postgres",
        password="postgres",
        host="localhost"
    )
    
    try:
        execute_sql_file(conn, "backend/db/criacao_tabelas.sql")
        
        operadoras_columns = [
            "registro_ans", "cnpj", "razao_social", "nome_fantasia", "modalidade",
            "logradouro", "numero", "complemento", "bairro", "cidade", "uf", "cep",
            "ddd", "telefone", "fax", "email", "representante", "cargo_representante",
            "data_registro_ans"
        ]
        import_csv_file(
            conn,
            "operadoras",
            "backend/db/dados_ans/operadoras_ativas.csv",
            operadoras_columns
        )
        
        demonstracoes_columns = [
            "registro_ans", "data", "conta", "descricao", "valor", "periodo"
        ]
        import_csv_file(
            conn,
            "demonstracoes",
            "backend/db/dados_ans/processed/demonstracoes_contabeis.csv",
            demonstracoes_columns
        )
        
        print("Seeding concluido com sucesso.")
        execute_sql_file(conn, "backend/db/consultas.sql", display_results=True)
        print("Consultas executadas com sucesso.")
    except Exception as e:
        print(f"Error during database seeding: {e}")
    finally:
        conn.close()