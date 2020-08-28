FROM mikematera/p4e-stack:release-20200730

USER $NB_UID
COPY --chown=jovyan:users . ${HOME}
RUN pip install -r requirements.txt 

ENV JUPYTER_ENABLE_LAB yes
