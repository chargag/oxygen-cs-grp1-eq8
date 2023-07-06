## Repéré à https://dev.to/mrpbennett/setting-up-docker-with-pipenv-3h1o
#FROM python:3.8-slim
#
#WORKDIR /oxygencs
#
#COPY Pipfile.lock .
#COPY Pipfile .
#
#RUN python -m pip install --upgrade pip
#RUN pip install pipenv
#RUN pipenv install --dev --system --deploy
#
#COPY ./src ./src
#COPY docker.env .env
#
## Creates a non-root user and adds permission to access the /oxygencs folder
#RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /oxygencs
#USER appuser
#
#CMD ["python", "src/main.py"]


###

# Repéré à https://github.com/GoogleContainerTools/distroless/blob/main/examples/python3-requirements/Dockerfile


##################################################################
# Build a virtualenv using the appropriate Debian release
# * Install python3-venv for the built-in Python3 venv module (not installed by default)
# * Install gcc libpython3-dev to compile C Python modules
# * In the virtualenv: Update pip setuputils and wheel to support building new packages
FROM debian:11-slim AS build
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes python3-venv gcc libpython3-dev && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip setuptools wheel

# Build the virtualenv as a separate step: Only re-execute this step when requirements.txt changes
FROM build AS build-venv
COPY requirements-docker.txt /requirements.txt
RUN /venv/bin/pip install --disable-pip-version-check -r /requirements.txt

# Copy the virtualenv into a distroless image
FROM gcr.io/distroless/python3-debian11
COPY --from=build-venv /venv /venv

COPY src src
COPY docker.env .env
WORKDIR /src
ENTRYPOINT ["/venv/bin/python3", "main.py"]

