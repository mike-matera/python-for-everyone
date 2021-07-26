FROM  ghcr.io/mike-matera/p4e-stack:stack-20200726

USER $NB_UID
COPY --chown=jovyan:users . ${HOME}
RUN pip install -r requirements.txt 

ENV JUPYTER_ENABLE_LAB yes
