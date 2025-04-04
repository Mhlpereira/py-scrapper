BEGIN;

CREATE TABLE IF NOT EXISTS operadoras (
    id SERIAL PRIMARY KEY,
    registro_ans VARCHAR(20) NOT NULL UNIQUE,
    cnpj VARCHAR(14),
    razao_social VARCHAR(255) NOT NULL,
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    logradouro VARCHAR(255),
    numero VARCHAR(20),
    complemento VARCHAR(100),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    uf CHAR(2),
    cep VARCHAR(8),
    ddd VARCHAR(2),
    telefone VARCHAR(9),
    fax VARCHAR(10),
    email VARCHAR(100),
    representante VARCHAR(100),
    cargo_representante VARCHAR(100),
    data_registro_ans DATE
);

CREATE TABLE IF NOT EXISTS demonstracoes (
    id SERIAL PRIMARY KEY,
    operadora_id INTEGER REFERENCES operadoras(id),
    data DATE NOT NULL,
    registro_ans VARCHAR(20) NOT NULL,
    conta VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    valor DECIMAL(15,2) NOT NULL,
    periodo VARCHAR(10) CHECK (periodo IN ('mensal', 'trimestral', 'anual'))
);

CREATE INDEX idx_demonstracoes_registro_ans ON demonstracoes(registro_ans);
CREATE INDEX idx_demonstracoes_data ON demonstracoes(data);
CREATE INDEX idx_demonstracoes_conta ON demonstracoes(conta);

COMMIT;