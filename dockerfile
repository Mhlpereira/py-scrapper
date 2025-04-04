FROM python:3.9 as backend

WORKDIR /app/backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend .

FROM node:23.8 as frontend

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend .

FROM python:3.9

WORKDIR /app

COPY --from=backend /app/backend /app/backend

COPY --from=frontend /app/frontend /app/frontend

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["make", "run-all"]