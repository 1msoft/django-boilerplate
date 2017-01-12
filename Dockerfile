FROM python:2.7

# install db-client
ENV MYSQL_MAJOR 5.7
ENV MYSQL_VERSION 5.7.11-1debian8
ARG WORKDIR=server

RUN echo "deb http://repo.mysql.com/apt/debian/ jessie mysql-${MYSQL_MAJOR}" > /etc/apt/sources.list.d/mysql.list \
    && apt-key adv --keyserver ha.pool.sks-keyservers.net --recv-keys A4A9406876FCBD3C456770C88C718D3B5072E1F5 \
    && apt-get update \
    && apt-get install -y --force-yes --no-install-recommends  mysql-client libmysqlclient-dev freetds-dev netcat \
	&& apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --gecos '' accuragen

# alias
RUN echo "alias dj='python manage.py'" >> /root/.bashrc \
    && echo "alias migrate='python manage.py migrate'" >> /root/.bashrc \
    && echo "alias makemigrations='python manage.py makemigrations'" >> /root/.bashrc \
    && echo "alias djshell='python manage.py shell'" >> /root/.bashrc 

# create directory and set workdir
RUN mkdir /var/webapps
RUN mkdir /var/webapps/${WORKDIR}
WORKDIR /var/webapps/${WORKDIR}


ADD ./requirements.txt /var/webapps/${WORKDIR}
RUN pip install --upgrade pip \
    && pip install virtualenv \
    && pip install -r ./requirements.txt


ADD . /var/webapps/${WORKDIR}

ADD ./scripts/docker-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
