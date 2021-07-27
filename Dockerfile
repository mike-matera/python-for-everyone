# 
# Build a Jupyter Stack specific for my Python for Everyone class. 
#

FROM docker.io/jupyter/scipy-notebook:lab-3.0.16
USER root
RUN apt update -y && apt install -y openssh-client wamerican tree && apt clean -y
USER $NB_UID
COPY --chown=jovyan:users . ${HOME}
RUN pip install -r requirements.txt
RUN jupyter labextension install ipycanvas @jupyterlab/git

ENV JUPYTER_ENABLE_LAB yes
