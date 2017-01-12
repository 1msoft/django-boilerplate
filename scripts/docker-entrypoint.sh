#!/bin/sh

set -e

PYTHON=/usr/local/bin/python
NETCAT=/bin/nc


# check project's development env , 
# 在开发环境中，默认将python库安装到源文件的 python_modules.
# 在.dockerignore忽略了python_modules， 在生产环境中docker镜像不包括该目录。
# 在开发时，workddir映射到外部，通过检测是否存在 python_modules可以确定是否开发环境。
if [ -d "python_modules" ]; then
    # exist, so activate project's env
    bash -C "source python_modules/bin/activate"
    PYTHON=./python_modules/bin/python
    python manage.py migrate
    #export DEBUG='True'
fi



# if no env setting, use service name as hostname
# limit: only one container of each service
# 当存在多个服务实例时，dns-hostname会包括所有实例的ip地址.
# 在这种情况下可以在docker-compose中加入link，然后在入口脚本中检测环境变量。
if [ -z "$DATABASE_PORT" ]; then
  export DATABASE_PORT=3306
  echo "export DATABASE_PORT=$DATABASE_PORT" >> /root/.bashrc
fi

if  [ -z "$DATABASE_HOST" ]; then
  export DATABASE_HOST=mysql
  echo "export DATABASE_HOST=$DATABASE_HOST"  >> /root/.bashrc
fi


if [ -z  "$REDIS_PORT" ]; then
  export REDIS_PORT=6379
  echo "export REDIS_PORT=$REDIS_PORT" >> /root/.bashrc
fi

if [ -z "$REDIS_HOST" ]; then
  export REDIS_HOST=redis
  echo "export REDIS_HOST=$REDIS_HOST"  >> /root/.bashrc
fi

# wait for database
echo -n "waiting for mysql $DATABASE_HOST:$DATABASE_PORT..."
while ! $NETCAT -w 1 -z $DATABASE_HOST $DATABASE_PORT >/dev/null 2>&1
do
  echo -n .
  sleep 1
done

# run all .sh && .py in init.d
# this folder mount from volume map
echo -n "waiting for system initialize..."

for f in /var/webapps/cloudag/init.d/*; do
  case "$f" in
    *.sh)  echo "$0: running $f"; . "$f" || true;;
    *.py) echo "$0: running $f"; $PYTHON $f || true;;
    *)     echo "$0: ignoring $f" ;;
  esac
  echo
done



# run command
exec "$@"