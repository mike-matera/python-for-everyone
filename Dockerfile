# 
# Build a Jupyter Stack specific for my Python for Everyone class. 
#

FROM quay.io/jupyter/scipy-notebook:lab-4.2.4
USER root
RUN apt update -y && apt install -y openssh-client wamerican tree && apt clean -y
USER $NB_UID
COPY --chown=jovyan:users . ${HOME}
RUN pip install -r requirements.txt

ENV JUPYTER_ENABLE_LAB yes
