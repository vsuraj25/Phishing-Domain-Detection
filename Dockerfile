FROM python:3.8
COPY . /app
WORKDIR /app
RUN pip install -r requirements_dev.txt
EXPOSE $PORT
CMD gunicorn --workers=1 --bind 0.0.0.0:$PORT app:app