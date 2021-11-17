FROM tiangolo/uwsgi-nginx-flask:python3.6 
#-alpine3.7
# FROM python:3
# RUN apk --update add bash nano
RUN pip install --upgrade pip
# ENV STATIC_URL /
# ENV STATIC_PATH /
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD app.py /
ADD src/config.py /
# ENV FLASK_APP=app
# CMD ["python3", "app.py"]
# RUN python3 app.py