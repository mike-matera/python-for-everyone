# 
# Build a Jupyter Stack specific for the Python for Everyone class. 
#

FROM jupyter/scipy-notebook 
USER root
RUN apt update -y && apt install -y openssh-client
USER $NB_UID
RUN conda install xeus-python
RUN pip install ipycanvas jupyterlab-git jupyterlab
RUN jupyter labextension install ipycanvas @jupyterlab/debugger @jupyterlab/git

ENV JUPYTER_ENABLE_LAB yes
