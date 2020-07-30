FROM mikematera/p4e-stack

COPY --chown=jovyan:users requirements.txt /home/jovyan/content/
COPY --chown=jovyan:users Lessons /home/jovyan/content/Lessons/
COPY --chown=jovyan:users Labs /home/jovyan/content/Labs/
COPY --chown=jovyan:users Packages /home/jovyan/content/Packages/
RUN cd /home/jovyan/content && pip install -r requirements.txt 
COPY --chown=jovyan:users jupyter_notebook_config.py /home/jovyan/.jupyter/

ENV JUPYTER_ENABLE_LAB yes
