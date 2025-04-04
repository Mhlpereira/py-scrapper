DB_NAME = ans_database
DB_USER = postgres
DB_PASSWORD = sua_senha
PSQL = PGPASSWORD=$(DB_PASSWORD) psql -h localhost -U $(DB_USER) -d $(DB_NAME)
MYSQL = mysql -u $(DB_USER) -p$(DB_PASSWORD) $(DB_NAME)

all: setup_db import_dados download_anexos formatando_dados
	@echo "Todos os passos concluídos com sucesso!"

setup: 
	@echo "🔧 Criando e ativando ambiente virtual..."
	test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)
	@echo "📦 Instalando dependências..."
	$(PIP) install -r backend/requirements.txt
	@echo "✅ Setup concluído! Para ativar o ambiente, execute 'source $(VENV_DIR)/bin/activate'"

setup-frontend:
	@echo "📦 Instalando dependências do frontend..."
	cd frontend && npm install

run-frontend: 
	@echo "🌐 Iniciando frontend..."
	cd frontend && npm run dev
	
download_anexos:
	@echo "Baixando anexos..."
	@cd backend/web-scraper && python scraper.py
	@echo "Baixando anexos..."

formatando_dados:
	@echo "Formatando dados..."
	@cd backend/web-scraper && python transform-data.py
	@echo "Formatando dados..."

download_dados:
	@echo "Baixando dados da ANS..."
	@cd backend/db && python scraper-3.py
	@echo "Download concluído!"

setup_db:  backend/db/criacao_tabelas.sql
	@echo "Criando estrutura do banco de dados..."
	@$(PSQL) -f $<  # Para PostgreSQL
	# @$(MYSQL) < $<  # Descomente para MySQL
	@echo "Estrutura criada com sucesso!"

import_dados: backend/db/importacao_postgres.sql
	@echo "Importando dados para o PostgreSQL..."
	@$(PSQL) -f $<
	# @$(MYSQL) < sql/importacao_mysql.sql  # Descomente para MySQL
	@echo "Dados importados com sucesso!"

run-backend: 
	@echo "🚀 Iniciando backend..."
	$(PYTHON) -m uvicorn app.main:app --reload
