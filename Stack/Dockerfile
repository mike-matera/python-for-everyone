# 
# Build a Jupyter Stack specific for the Python for Everyone class. 
#

FROM docker.io/jupyter/scipy-notebook:lab-3.0.16
USER root
RUN apt update -y && apt install -y openssh-client wamerican tree && apt clean -y
USER $NB_UID
# RUN conda install -y xeus-python && conda clean -y --all
RUN pip install ipycanvas jupyterlab-git jupyterlab sql ipython-sql folium
RUN jupyter labextension install ipycanvas @jupyterlab/debugger @jupyterlab/git

ENV JUPYTER_ENABLE_LAB yes
