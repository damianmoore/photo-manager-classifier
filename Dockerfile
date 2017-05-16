FROM caffe2ai/caffe2:c2.cpu.ubuntu14.04

RUN apt-get update && \
    apt-get install -y supervisor gunicorn nginx-light && \
        apt-get clean && \
            rm -rf /var/lib/apt/lists/* \
                   /tmp/* \
                   /var/tmp/*

# Install Python dependencies
COPY frontend-web/requirements.txt /srv/frontend-web/requirements.txt
RUN pip install -vU setuptools pip
RUN pip install -r /srv/frontend-web/requirements.txt

COPY frontend-web /srv/frontend-web

COPY run.sh /srv/run.sh
COPY supervisord.conf /etc/supervisord.conf
COPY nginx.conf /etc/nginx/nginx.conf

WORKDIR /srv
CMD ./run.sh

EXPOSE 80
