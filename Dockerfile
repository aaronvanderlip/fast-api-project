FROM python:3.12.6-alpine3.20

WORKDIR /usr/src/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src
COPY ./pyproject.toml /usr/src
COPY ./app/celeryconfig.py /usr/src
COPY ./README.md /usr/src
RUN pip install -r /usr/src/requirements.txt

COPY ./app /usr/src/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
