FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app
ENV SEED_ON_STARTUP: 1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend code
COPY . .

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

