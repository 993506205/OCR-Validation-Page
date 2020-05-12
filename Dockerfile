FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /Ocr
WORKDIR /Ocr
COPY requirements.txt /Ocr/
RUN pip install -r requirements.txt
COPY . /Ocr/