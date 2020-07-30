FROM mikematera/python-for-everyone:test3

COPY --chown=jovyan:users Lessons /home/jovyan/Lessons
COPY --chown=jovyan:users Labs /home/jovyan/Labs
COPY --chown=jovyan:users Packages /home/jovyan/Packages
COPY --chown=jovyan:users requirements.txt /home/jovyan/
RUN pip install -r /home/jovyan/requirements.txt 

ENV JUPYTER_ENABLE_LAB yes
