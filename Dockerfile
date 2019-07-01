FROM python:3.7.3-alpine3.9


RUN apk add --no-cache postgresql-client postgresql-dev gcc musl-dev

RUN mkdir -p /apply/cmdb
ADD ./ /apply/cmdb/
RUN pip --no-cache-dir install -r /apply/cmdb/requirements.txt


WORKDIR /apply/cmdb/

EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
