FROM python:3.11
WORKDIR /code
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /code/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install -r /code/requirements.txt
COPY . /code
RUN chmod a+x docker/*.sh

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["python", "main.py"]