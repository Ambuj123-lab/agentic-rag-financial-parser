# ==================================
# Stage 1: Build Frontend (React + Vite)
# ==================================
FROM node:18-alpine AS frontend-build

WORKDIR /app/frontend

# Install dependencies (cached layer)
COPY frontend/package.json ./
COPY frontend/package-lock.json ./
RUN npm ci

# Build the project — empty VITE_API_URL = same-origin (no CORS in prod)
COPY frontend/ ./
ENV VITE_API_URL=""
RUN npm run build


# ==================================
# Stage 2: Setup Backend (FastAPI)
# ==================================
FROM python:3.11-slim AS backend

WORKDIR /app

# Install system dependencies (needed for grpcio compilation)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies — no-cache-dir keeps image small
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY app/ ./app/

# Copy built frontend assets from Stage 1
COPY --from=frontend-build /app/frontend/dist ./frontend/dist

# Environment variables
ENV PYTHONUNBUFFERED=1

# Expose port (default 8000, Render overrides via $PORT)
EXPOSE 8000

# Command to run (shell form to support dynamic $PORT from Render)
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
