# Use the official Python base image
FROM python:3.11 as base

ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory
WORKDIR /app

ENV PYTHON=value

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH=$PATH:/root/.local/bin

COPY app/pyproject.toml .
COPY app/poetry.lock .

# Install project dependencies using Poetry
RUN poetry install --no-root

# Copy the application code
COPY app .

FROM base as migration

CMD poetry run python manage.py makemigrations main &&\
    poetry run python manage.py migrate

FROM base as development

EXPOSE 8080

CMD poetry run python manage.py runserver 0.0.0.0:8080