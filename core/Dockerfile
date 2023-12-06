FROM python:3.12-slim
COPY pyproject.toml .
COPY poetry.lock .
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
ADD base_mqtt_pub_sub.py .
ADD base_mqtt_pub_sub_test.py .
