FROM python:3.7-alpine

ADD msa_sdk /python_sdk/msa_sdk
WORKDIR /python_sdk

ADD requirements.txt /python_sdk

RUN pip install -r requirements.txt
