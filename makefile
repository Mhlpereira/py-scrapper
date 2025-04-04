PYTHON = backend/venv/bin/python

DB_NAME = ans_database
DB_USER = postgres
DB_PASSWORD = postgres
PSQL = PGPASSWORD=postgres psql -h localhost -U $(DB_USER)  -d $(DB_NAME)

.PHONY: all 

all: setup setup-db download_anexos formatando_dados executando_dados formatando_dados_demonstracao seed-db setup-frontend run-all

setup:
	
	@echo "Configurando ambiente..."
	cd backend && python3 -m venv venv
	backend/venv/bin/pip install --upgrade pip
	backend/venv/bin/pip  install -r backend/requirements.txt
	@echo "Setup concluído!"

setup-frontend:
	@echo " Instalando dependências do frontend..."
	cd frontend && npm install

setup-db:
	@echo " Configurando banco de dados..."
	docker compose up -d db
	sleep 5
	@echo " Banco de dados configurado!"

download_anexos:
	@echo " Baixando anexos..."
	$(PYTHON) backend/web-scraper/scraper.py

formatando_dados:
	@echo " Formatando dados..."
	$(PYTHON) backend/web-scraper/transform-data.py

formatando_dados_demonstracao:
	@echo " Formatando dados contabeis..."
	$(PYTHON) backend/db/transform-cont.py

executando_dados:
	@echo " Executando dados..."
	$(PYTHON) backend/db/scraper-3.py

seed-db:
	@echo " Seeding..."
	$(PYTHON) backend/db/seed-db.py

run-backend:
	@echo " Iniciando backend..."
	$(PYTHON) -m uvicorn backend.app.main:app --reload

run-frontend:
	@echo " Iniciando frontend..."
	cd frontend && npm run dev &

run-all: run-frontend run-backend
