FROM python:3.11.1-slim

RUN pip install "poetry==1.3.1"

COPY ./pyproject.toml /pyproject.toml
COPY ./poetry.lock /poetry.lock
RUN poetry config virtualenvs.create false && poetry install --no-root

COPY ./app /app
CMD ["python", "app/service.py"]

