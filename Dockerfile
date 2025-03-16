# Stage 1: Build the frontend
FROM node:22-slim AS frontend-builder
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Set up the Python environment
FROM python:3.12-slim
WORKDIR /app

# Copy the built frontend files
COPY --from=frontend-builder /app/dist /app/frontend/dist
RUN mkdir /app/storage

# Copy the Python script and API files
COPY backend/ /app/backend/

# Install Python dependencies
RUN pip install -r /app/backend/requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Command to run the Python script
CMD ["python", "/app/backend/serve.py"]
