FROM ciscotestautomation/pyats:latest-full
ENV VIRTUAL_ENV=/pyats
# RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt $VIRTUAL_ENV/requirements.txt

RUN pip install -r $VIRTUAL_ENV/requirements.txt

# CMD ["python3"]