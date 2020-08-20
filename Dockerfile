FROM python:latest

RUN mkdir /code
COPY requirements.txt /code
RUN pip install -r /code/requirements.txt
COPY . /code
WORKDIR /code
CMD python manage.py runserver 0.0.0.0:8000
