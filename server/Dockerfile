FROM python:3.11-slim

WORKDIR /server

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH="/server/src"

EXPOSE 8000

COPY ["./pyproject.toml", "./src/alembic.ini", "./"]
COPY ["./src", "/server/src"]
RUN pip install poetry && poetry install

WORKDIR /server/src

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
