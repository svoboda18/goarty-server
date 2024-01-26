# Dockerfile

FROM mcr.microsoft.com/devcontainers/base:ubuntu-18.04

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["python", "manage.py", "runserver"]