FROM python:3.6

WORKDIR /usr/src/lm_test

COPY ./ ./

RUN apt install git

RUN git clone https://github.com/specify/open_api_tools/

RUN pip install --no-cache-dir -r open_api_tools/requirements.txt

RUN pip install -e open_api_tools/

CMD /bin/sh

