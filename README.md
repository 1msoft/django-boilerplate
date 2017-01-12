# django-boilerplate

### docker file
```
docker build . -t xxxx/xxx:xxx  --build-arg WORKDIR=XXX 
```
WORKDIR has default value eq "server"

### docker-compose
.env file  WEB_ENV=development or production
config/envfile/mysql  mysql's env setting
config/envfile/development.env , web service's env setting for development
config/mysql/my.cnf : mysql config file, for utf8 charset

### nativate-develop
start_env.sh : config localhost development 

### setting.py
load all from env
