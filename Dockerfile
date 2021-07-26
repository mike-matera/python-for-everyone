FROM  ghcr.io/mike-matera/p4e-stack:stack-20200726

RUN cd /home/jovyan/content && pip install --user -r requirements.txt 
RUN cd /home/jovyan/content/tools && pip install --user -e . 
