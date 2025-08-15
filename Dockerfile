# 
# Build a Jupyter Stack specific for my Python for Everyone class. 
#
ARG PYTHON_VERSION=3.12
ARG DEBIAN_VERSION=slim-bookworm

FROM docker.io/python:${PYTHON_VERSION}-${DEBIAN_VERSION}

RUN apt update -y && apt install -y wget tree pandoc git && apt clean -y

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ARG NB_UID="1000"
ARG NB_USER="student" 

# Create the student user
ENV NB_UID=${NB_UID} \
    NB_USER=${NB_USER}
RUN useradd --no-log-init --create-home --shell /bin/bash --uid ${NB_UID} ${NB_USER}
USER ${NB_USER}

# Install Python dependencies
ADD --chown=${NB_UID}:${NB_UID} pyproject.toml uv.lock /home/p4e/
WORKDIR /home/p4e
RUN uv sync --locked

# Install notebooks
ADD --chown=${NB_UID}:${NB_UID} . /home/${NB_USER}
WORKDIR /home/${NB_USER}

# Cleanup 
RUN rm -rf uv.lock pyproject.toml

ENV PATH="/home/p4e/.venv/bin:$PATH" \
    JUPYTER_ENABLE_LAB=yes \
    SHELL=/bin/bash
