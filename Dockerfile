#init from python
FROM python:3.11.15-slim-trixie

WORKDIR /fastapiapp

COPY . .
RUN pip install -r requirements.txt

#run this command while running the container
CMD uvicorn app:fastapi --reload --host=0.0.0.0
