FROM python:3
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

## Uncomment if using requirements.txt
COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

COPY . /app/

ENV FLASK_APP=app
EXPOSE 5000

# configure the container to run in an executed manner
CMD ["python" , "app.py" ]