FROM jupyter/base-notebook

USER root
RUN pip install netmiko
RUN mkdir /pkg
ADD setup.py /pkg/
ADD msa_sdk/ /pkg/msa_sdk

RUN pip install -e /pkg/

USER jovyan
ADD jupyter_notebook_config.py $HOME/.jupyter/