FROM mikematera/python-for-everyone:test3

COPY --chown=jovyan:users Lessons /home/jovyan/Lessons
COPY --chown=jovyan:users Labs /home/jovyan/Labs
COPY --chown=jovyan:users p4e /home/jovyan/p4e
COPY --chown=jovyan:users requirements.txt setup.py requirements.txt /home/jovyan/
RUN pip install -r /home/jovyan/requirements.txt 
RUN pip install -e /home/jovyan  

ENV JUPYTER_ENABLE_LAB yes
