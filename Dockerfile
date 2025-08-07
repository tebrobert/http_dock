FROM python:3.10.18

WORKDIR /usr/src/app

RUN pip install flask
COPY * ./

CMD [ "python", "./flask_app_stories.py" ]
EXPOSE 4000
