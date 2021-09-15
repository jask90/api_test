FROM python:3.8-slim-buster
ARG DEBIAN_FRONTEND=noninteractive

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /opt/api_test
WORKDIR /opt/api_test

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3-pip

RUN pip3 install -r requirements.txt

COPY ./entrypoint.sh entrypoint.sh

RUN chmod +x entrypoint.sh && \
    ./entrypoint.sh

EXPOSE 8000

CMD ["python3", "/opt/api_test/df_drf/manage.py", "runserver", "0.0.0.0:8000"]
