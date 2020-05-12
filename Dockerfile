FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /Ocr
WORKDIR /Ocr/
RUN apt update && apt install tesseract-ocr && apt install libtesseract-dev
COPY requirements.txt /Ocr/
RUN pip install -r requirements.txt
COPY . /Ocr/