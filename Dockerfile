FROM jupyter/scipy-notebook

RUN conda install xeus-python
RUN pip install ipycanvas 
RUN jupyter labextension install ipycanvas @jupyterlab/debugger

COPY --chown=jovyan:users . /home/jovyan/
RUN pip install -r /home/jovyan/requirements.txt 

ENV JUPYTER_ENABLE_LAB yes
