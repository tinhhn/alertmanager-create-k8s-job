FROM python:slim

WORKDIR /app

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD alertmanager-trigger-k8s-cronjob.py .

CMD gunicorn -w 4 -b 0.0.0.0:5000 --access-logfile - alertmanager-trigger-k8s-cronjob:app
