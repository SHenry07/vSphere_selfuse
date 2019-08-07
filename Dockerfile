FROM 192.168.100.235/python/python:3.7.3-alpine3.9


RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories; \
apk update; \
apk add --no-cache  gcc musl-dev mysql-dev libffi-dev

RUN mkdir -p /apply/cmdb/logs
ADD ./ /apply/cmdb/
RUN pip --no-cache-dir install -r /apply/cmdb/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


WORKDIR /apply/cmdb/

EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
