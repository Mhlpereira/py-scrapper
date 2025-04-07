# Sistema de Análise de Dados de Operadoras de Planos de Saúde ANS

## Visão Geral
Este sistema processa e analisa dados da ANS (Agência Nacional de Saúde Suplementar), com foco em operadoras de planos de saúde e suas demonstrações financeiras.

## Configuração e Execução

### Pré-requisitos
- Docker 
- Utilitáro Make
- PlSql 

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
- Dados abertos de rol de procedimento: https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-
sociedade/atualizacao-do-rol-de-procedimentos
- Dados das operadoras de planos de saúde: https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/
- Demonstrações financeiras (últimos 2 anos): https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/

## Análises Disponíveis
- Top 10 operadoras por despesas no último trimestre
- Top 10 operadoras por despesas no último ano
- Visualizações adicionais disponíveis através da interface web

