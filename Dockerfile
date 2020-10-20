FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
RUN apk --update add bash nano
RUN pip install --upgrade pip
RUN pip3 install --upgrade cython
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
ENV STATIC_URL /static
ENV STATIC_PATH /static
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD app.py /
# ENV FLASK_APP=app.py:app
CMD ["python3", "./app.py"]