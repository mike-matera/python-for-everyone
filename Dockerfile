# 
# Build a Jupyter Stack specific for my Python for Everyone class. 
#

FROM quay.io/jupyter/scipy-notebook:lab-4.2.4
USER root
RUN apt update -y && apt install -y openssh-client wamerican tree && apt clean -y
USER $NB_UID
COPY --chown=jovyan:users . ${HOME}
RUN pip install -r requirements.txt

# Autoload my extensions.
RUN ipython profile create default
#COPY <<EOF ${HOME}/.ipython/profile_default/ipython_config.py
#c = get_config()  # noqa: F821
#c.InteractiveShellApp.extensions.append('doctags')
#EOF

ENV JUPYTER_ENABLE_LAB yes
