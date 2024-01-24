# 
# Build a Jupyter Stack specific for my Python for Everyone class. 
#

FROM docker.io/jupyter/scipy-notebook:hub-4.0.2
USER root
RUN apt update -y && apt install -y openssh-client wamerican tree && apt clean -y
USER $NB_UID
COPY --chown=jovyan:users . ${HOME}
RUN pip install -r requirements.txt

# Autoload my extensions.
RUN ipython profile create default
COPY <<EOF ${HOME}/.ipython/profile_default/ipython_config.py
c = get_config()  # noqa: F821
c.InteractiveShellApp.extensions.append('nb_introspect')
EOF

ENV JUPYTER_ENABLE_LAB yes
