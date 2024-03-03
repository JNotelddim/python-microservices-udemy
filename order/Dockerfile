FROM python:3.10

COPY requirements.txt /orderapp/requirements.txt

WORKDIR /orderapp
RUN pip install -r requirements.txt
COPY . /orderapp

ENTRYPOINT [ "python" ]
CMD ["app.py"]