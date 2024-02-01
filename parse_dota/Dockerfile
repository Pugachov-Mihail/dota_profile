FROM python:3.11
WORKDIR /parse
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /parse/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install -r /parse/requirements.txt
COPY . /parse
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]