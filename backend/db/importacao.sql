\copy operadoras (
    registro_ans, cnpj, razao_social, nome_fantasia, modalidade,
    logradouro, numero, complemento, bairro, cidade, uf, cep,
    ddd, telefone, fax, email, representante, cargo_representante,
    data_registro_ans
) 
FROM 'dados/cadastro/operadoras_ativas.csv' 
WITH (FORMAT CSV, DELIMITER ';', HEADER true, ENCODING 'LATIN1');


\copy demonstracoes (registro_ans, data, conta, descricao, valor, periodo)
FROM 'dados/demonstracoes/2023/Demonstrações_Contábeis_202301.csv'
WITH (FORMAT CSV, DELIMITER ';', HEADER true, ENCODING 'LATIN1');