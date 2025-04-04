# Sistema de Análise de Dados de Operadoras de Planos de Saúde ANS

## Visão Geral
Este sistema processa e analisa dados da ANS (Agência Nacional de Saúde Suplementar), com foco em operadoras de planos de saúde e suas demonstrações financeiras.

## Configuração e Execução

### Pré-requisitos
- Docker e Docker Compose
- Utilitário Make
- Cliente PostgreSQL (para inspeção manual do banco de dados)

### Início Rápido
Execute toda a configuração do sistema com um único comando:
```bash
make all
```

Este comando irá:
1. Configurar os contêineres Docker
2. Baixar os dados necessários dos repositórios públicos da ANS
3. Processar e importar os dados para o PostgreSQL
4. Executar consultas analíticas

### Acesso ao Banco de Dados
Para inspecionar o banco de dados diretamente usando o cliente PostgreSQL:
```bash
PGPASSWORD=postgres psql -h localhost -U postgres -d ans_database
```

### Interface Web
Acesse o painel de visualização de dados em:
```
http://localhost:5173/
```

## Fontes de Dados
- Dados das operadoras de planos de saúde: https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/
- Demonstrações financeiras (últimos 2 anos): https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/

## Estrutura do Projeto
- `backend/db/seed-db.py`: Script principal para configuração do banco de dados e importação de dados
- `backend/db/create_tables.sql`: Definições SQL para tabelas do banco de dados
- `backend/db/consultas.sql`: Consultas analíticas
- `backend/db/dados_ans/`: Diretório contendo dados ANS baixados e processados

## Análises Disponíveis
- Top 10 operadoras por despesas no último trimestre
- Top 10 operadoras por despesas no último ano
- Visualizações adicionais disponíveis através da interface web

## Solução de Problemas
Se você encontrar erros de caminho de arquivo durante a importação, verifique se os arquivos CSV estão no local correto e possuem a codificação adequada (LATIN1).
