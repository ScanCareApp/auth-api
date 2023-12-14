#masi kopas dari repo sebelah hehehe 
FROM python:3.10.3-slim-buster

WORKDIR /workspace

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

ENV PORT 8000

ENV HOST 0.0.0.0

CMD ["python", "main.py"]
