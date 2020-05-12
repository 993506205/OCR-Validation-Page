FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /Ocr
WORKDIR /Ocr/
RUN apt update && apt install tesseract-ocr -y && apt install libtesseract-dev -y
COPY requirements.txt /Ocr/
RUN pip install -r requirements.txt
COPY . /Ocr/