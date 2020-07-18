FROM mikematera/python-for-everyone

COPY --chown=jovyan:users . /home/jovyan/
RUN pip install -r /home/jovyan/requirements.txt 

ENV JUPYTER_ENABLE_LAB yes
