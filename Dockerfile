# ==============================================================================
# Railnex AI — Multi-Stage Production Dockerfile
# Stage 1: Build the React 18 + TypeScript + Tailwind CSS Frontend SPA
# Stage 2: High-Performance Python 3.11 FastAPI Decision-Support API Server
# ==============================================================================

# ----------------- Stage 1: Frontend Build -----------------
FROM node:20-alpine AS frontend-builder
WORKDIR /build

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build

# ----------------- Stage 2: Production Runtime -------------
FROM python:3.11-slim AS runtime

# System runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Backend, Models, Scripts, and Validated Data
COPY backend/ ./backend/
COPY models/ ./models/
COPY scripts/ ./scripts/
COPY TrackPrior-AI/ ./TrackPrior-AI/

# Copy compiled frontend SPA from Stage 1
COPY --from=frontend-builder /build/dist ./frontend/dist

# Expose FastAPI Web Server Port
EXPOSE 8000

ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0
ENV PORT=8000

# Health check probe
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/api/health || exit 1

# Start Railnex AI Unified Server
CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
