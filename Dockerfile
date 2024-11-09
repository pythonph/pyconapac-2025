FROM python:3.10

ENV PYTHONUNBUFFERED=1

RUN mkdir -p /usr/src/app

COPY requirements.txt /usr/src/app
RUN pip install -r /usr/src/app/requirements.txt

COPY . /usr/src/app
WORKDIR /usr/src/app

RUN python manage.py collectstatic --noinput

EXPOSE 80

CMD ["gunicorn", "--bind", "0.0.0.0:80", "--access-logfile", "-", "--error-logfile", "-", "config.wsgi"]
