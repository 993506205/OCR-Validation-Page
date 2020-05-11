FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /ocr-project
WORKDIR /ocr-project
COPY requirements.txt /ocr-project/
RUN pip install -r requirements.txt
COPY . /ocr-project/