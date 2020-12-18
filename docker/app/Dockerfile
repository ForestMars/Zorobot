FROM python:3.8.3-slim

COPY app.py /app/
COPY docker/bot/files /app/files/
COPY nginx/zorobot /etc/nginx/sites-available/

WORKDIR /app

RUN apt-get -y update
RUN apt-get install -y python3-dev python3-pip nginx
RUN python3 -m pip install -r requirements.txt
RUN ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled
RUN systemctl restart nginx

ARG FLASK_RUN_PORT
ENV FLASK_RUN_PORT $FLASK_RUN_PORT

CMD ["python3", "./app.py", "port=${FLASK_RUN_PORT}"]
