FROM python:3.6-alpine

RUN adduser -D flask-app

WORKDIR /home/flask_app/

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY flask-app.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP flask-app.py

RUN chown -R flask-app:flask-app ./
USER flask-app

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
