FROM python:3
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

## Uncomment if using requirements.txt
COPY requirements.txt /code/
RUN pip3 install -r requirements.txt

COPY . /code/

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["app.py" ]