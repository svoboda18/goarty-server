# Dockerfile

FROM python:3.8

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN sudo apt-get install openjdk-17-jdk-headless openjdk-17-jdk openjdk-17-jre-headless openjdk-17-jre

COPY . /app/

CMD ["python", "manage.py", "runserver"]