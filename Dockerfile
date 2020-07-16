FROM jupyter/scipy-notebook

RUN conda install xeus-python
RUN jupyter labextension install ipycanvas @jupyterlab/debugger
RUN pip install ipycanvas 

COPY Lesson* /home/jovyan/notebooks/

ENV JUPYTER_ENABLE_LAB yes
