FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN apt update && apt install -y \
      gettext \
      python3-dev \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /code/static
WORKDIR /code
COPY Pipfile /code/
RUN pip install pipenv && pipenv install
COPY . /code/
ENTRYPOINT ["/code/entrypoint.sh"]

