# Repéré à https://dev.to/mrpbennett/setting-up-docker-with-pipenv-3h1o
FROM python:3.8-slim

WORKDIR /oxygencs

COPY Pipfile.lock .
COPY Pipfile .

RUN python -m pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --dev --system --deploy

COPY ./src ./src
COPY docker.env .env

# Creates a non-root user and adds permission to access the /oxygencs folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /oxygencs
USER appuser

CMD ["python", "src/main.py"]
