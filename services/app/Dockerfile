FROM ubuntu:16.04

MAINTAINER Mist13rios "k_timukov@mail.ru"

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=newt
ENV SYSTEM_USER django
ENV SYSTEM_GROUP webapp

# Install python3.6
RUN apt-get update \
    && apt-get install -y --no-install-recommends software-properties-common \
    && add-apt-repository -y ppa:deadsnakes \
    && apt-get update \
    && apt-get install -q -y --no-install-recommends python3.6 python3.6-dev python3-pip python3-setuptools python3-wheel gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
# set python 3.6 as the default python version
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.6 1 \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1 \
    && update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1
RUN pip3 install --upgrade pip requests setuptools

RUN apt-get update && apt-get install -y --no-install-recommends \
    nano \
    curl \
    make \
    gosu \
    gnupg2 \
    libtool \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    libevent-dev \
    libssl-dev \
    libbz2-dev \
    libreadline-dev \
    libmagic-dev \
    libncurses-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libopenblas-dev \
    liblapack-dev \
    libgeoip-dev \
    locales \
    mc \
    libcairo2 \
    libcairo2-dbg \
    gettext \
    wkhtmltopdf \
    libmaxminddb0 \
    libmaxminddb-dev \
    mmdb-bin \
    && rm -rf /var/lib/apt/lists/*

RUN localedef -i en_US -c -f UTF-8 en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN curl -sL https://deb.nodesource.com/setup_8.x | bash - && \
    apt-get update && \
    rm -rf /var/lib/apt/lists/*

RUN bash -c 'mkdir -p /var/www/{env,src,logs/static/temp}'

RUN adduser $SYSTEM_USER
RUN addgroup $SYSTEM_GROUP
RUN pip install --no-cache-dir virtualenv && \
    /usr/local/bin/virtualenv /var/www/env && \
    chown -R $SYSTEM_USER:$SYSTEM_GROUP /var/www

COPY ./requirements /var/www/src/requirements
COPY ./static /var/www/src/static

ARG REQUIREMENTS=base
RUN gosu $SYSTEM_USER bash -c "\
    source /var/www/env/bin/activate && \
    pip install --no-cache-dir -r /var/www/src/requirements/${REQUIREMENTS}.txt"

COPY frontend /var/www/src/frontend

WORKDIR /var/www/src

ARG BUILD_ENV=production

COPY ./services/app/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

COPY . /var/www/src/
RUN chown -R $SYSTEM_USER:$SYSTEM_GROUP /var/www/src

VOLUME ["/var/www/src", "/var/www/logs"]

EXPOSE 8080

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["gunicorn", "main.wsgi:application"]
