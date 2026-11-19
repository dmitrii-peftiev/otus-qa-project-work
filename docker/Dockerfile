FROM jenkins/jenkins:lts

USER root

ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

COPY requirements.txt /tmp/requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
        libatomic1 \
        python3-pip \
    && pip3 install --no-cache-dir --break-system-packages \
        -r /tmp/requirements.txt \
    && playwright install --with-deps chromium \
    && rm -rf \
        /tmp/requirements.txt \
        /var/lib/apt/lists/*

USER jenkins
