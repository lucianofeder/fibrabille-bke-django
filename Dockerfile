FROM python:3.8.5

EXPOSE 8000

ADD . /deploy

WORKDIR /deploy

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD python manage.py runserver 0.0.0.0:8000
