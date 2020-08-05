ARG VARIANT=3
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

LABEL maintainer="Quinn Snyder <qsnyder@cisco.com> (from Eric Thiel original <erthiel@cisco.com>)"

COPY requirements.txt . 

ENV info "ACI-Development v3.7.6: Python 3.7.6, Ansible 2.9.5, Openconnect, VIRLUtils, ACIToolkit, COBRA"

RUN echo 'PS1="\[\e[36m\]\u\[\e[m\]\[\e[37m\]@\[\e[m\]\[\e[32m\]dnebase376\[\e[m\]:\[\e[33m\]\w\[\e[m\]\[\e[33m\]\\$\[\e[m\] "' >> /root/.bashrc 

RUN apt-get update && \
    apt-get install -y make curl bash git gcc musl-dev libffi-dev libxml2-dev libxslt-dev wget && \
    python -m ensurepip && \
    pip install --upgrade pip setuptools && \
    pip install -r requirements.txt && \
    wget https://d1nmyq4gcgsfi5.cloudfront.net/fileMedia/1f3d41ce-d154-44e3-74c1-d6cf3b525eaa/acicobra-4.2_3h-py2.py3-none-any.whl -P /tmp/ && \
    wget https://d1nmyq4gcgsfi5.cloudfront.net/fileMedia/b3b69aa3-891b-41ff-46db-a73b4b215860/acimodel-4.2_3h-py2.py3-none-any.whl -P /tmp/ && \
    pip install /tmp/acicobra-4.2_3h-py2.py3-none-any.whl && \
    pip install /tmp/acimodel-4.2_3h-py2.py3-none-any.whl && \
    mkdir /acitoolkit && \
    mkdir /arya && \
    mkdir /webarya && \
    git clone --depth=1 https://github.com/qsnyder/acitoolkit.git /acitoolkit/ && \
    cd /acitoolkit && \
    python setup.py install && \
    git clone  --depth=1 https://github.com/qsnyder/arya.git /arya/ && \
    cd /arya && \
    python setup.py install && \
    git clone --depth=1 https://github.com/qsnyder/webarya.git /webarya/ && \
    cd /webarya/ && \
    pip install -r requirements.txt && \
    apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* /tmp/library-scripts && \
    rm -rf /tmp/pip-tmp && \
    rm -r /root/.cache

EXPOSE 80/tcp

CMD ["/bin/bash"]