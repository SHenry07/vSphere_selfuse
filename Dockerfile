FROM python:3.7.3


RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories; \
sed -i '$a */30 * * * * root python3 /apply/cmdb/manage.py ldap_sync_users' /etc/crontab;\
sed -i '$a * 2 * * * root python3 /apply/cmdb/apps/cronupdatevmdb.py' /etc/crontab;\
apk update; \
apk add --no-cache  gcc musl-dev mysql-dev libffi-dev build-base openldap-dev  python3-dev

RUN mkdir -p /apply/cmdb/logs
ADD ./ /apply/cmdb/
RUN pip --no-cache-dir install -r /apply/cmdb/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


WORKDIR /apply/cmdb/

EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
