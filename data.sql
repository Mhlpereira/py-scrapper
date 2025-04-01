CREATE TABLE operadoras (
    registro_ans VARCHAR(20) PRIMARY KEY,
    cnpj VARCHAR(20),
    razao_social VARCHAR(255),
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    logradouro VARCHAR(255),
    numero VARCHAR(20),
    complemento VARCHAR(100),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    uf CHAR(2),
    cep VARCHAR(10),
    ddd VARCHAR(5),
    telefone VARCHAR(20),
    fax VARCHAR(20),
    email VARCHAR(100),
    representante VARCHAR(255),
    cargo_representante VARCHAR(100),
    data_registro_ans DATE
);

CREATE TABLE demonstracoes_contabeis (
    id SERIAL PRIMARY KEY,
    registro_ans VARCHAR(20),
    data_ano INT,
    data_trimestre INT,
    codigo_conta VARCHAR(50),
    descricao_conta VARCHAR(255),
    valor_conta NUMERIC(15, 2),
    FOREIGN KEY (registro_ans) REFERENCES operadoras(registro_ans)
);

COPY operadoras FROM '/path/to/database_files/Relatorio_Cadop.csv' 
WITH (FORMAT CSV, HEADER, DELIMITER ';', ENCODING 'LATIN1');


CREATE OR REPLACE FUNCTION import_financial_data(file_path TEXT, year INT, quarter INT) 
RETURNS VOID AS $$
BEGIN
    EXECUTE format('
        COPY demonstracoes_contabeis(registro_ans, codigo_conta, descricao_conta, valor_conta) 
        FROM %L 
        WITH (FORMAT CSV, HEADER, DELIMITER '';'', ENCODING ''LATIN1'');
        
        UPDATE demonstracoes_contabeis 
        SET data_ano = %s, data_trimestre = %s
        WHERE data_ano IS NULL AND data_trimestre IS NULL;
    ', file_path, year, quarter);
END;
$$ LANGUAGE plpgsql;

WITH last_quarter AS (
    SELECT MAX(data_ano) as year, MAX(data_trimestre) as quarter
    FROM demonstracoes_contabeis
    WHERE data_ano = (SELECT MAX(data_ano) FROM demonstracoes_contabeis)
)
SELECT o.razao_social, SUM(dc.valor_conta) as total_despesa
FROM demonstracoes_contabeis dc
JOIN operadoras o ON dc.registro_ans = o.registro_ans
JOIN last_quarter lq ON dc.data_ano = lq.year AND dc.data_trimestre = lq.quarter
WHERE dc.descricao_conta = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'
GROUP BY o.razao_social
ORDER BY total_despesa DESC
LIMIT 10;

WITH last_year AS (
    SELECT MAX(data_ano) as year
    FROM demonstracoes_contabeis
)
SELECT o.razao_social, SUM(dc.valor_conta) as total_despesa
FROM demonstracoes_contabeis dc
JOIN operadoras o ON dc.registro_ans = o.registro_ans
JOIN last_year ly ON dc.data_ano = ly.year
WHERE dc.descricao_conta = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'
GROUP BY o.razao_social
ORDER BY total_despesa DESC
LIMIT 10;