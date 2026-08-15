#init from python
FROM python:3.11.15-slim-trixie

WORKDIR /fastapiapp

#copy requirements.txt and install all dependent libraries
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

#copy all other required files to Docker Image
COPY app.py model.joblib Dockerfile compose.yml ./

#Docker will execute this command while running the container
CMD uvicorn app:fastapi --reload --host=0.0.0.0
