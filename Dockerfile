FROM mikematera/p4e-stack:release-20200730

USER $NB_UID
COPY requirements.txt /home/jovyan/content/
COPY Lessons /home/jovyan/content/Lessons/
COPY Labs /home/jovyan/content/Labs/
COPY Packages /home/jovyan/content/Packages/
COPY jupyter_notebook_config.py /home/jovyan/.jupyter/
COPY welcome.ipynb /home/jovyan/welcome.ipynb
RUN cd /home/jovyan/content && pip install -r requirements.txt 

ENV JUPYTER_ENABLE_LAB yes
