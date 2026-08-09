FROM python:3.11-slim

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy src folder since it has contents we need 
COPY ./src ./src
# Copy fastapi app code to working directory
COPY ./labeling_app ./labeling_app

# Set python path to correctly resolve imports
ENV PYTHONPATH=/app/src

# Expose the application port
EXPOSE 8000

# Start FastAPI using the standard CLI command
CMD ["uvicorn", "labeling_app.main:app", "--host", "0.0.0.0", "--port", "8000"]