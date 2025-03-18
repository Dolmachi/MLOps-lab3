FROM python:3.12

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install --no-cache-dir ansible

COPY vault-key /app/
COPY secrets.yml /app/

RUN ansible-vault decrypt secrets.yml --output secrets.yml --vault-password-file /app/vault-key

RUN rm -f /app/vault-key

COPY . /app

RUN pip install -r requirements.txt

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]