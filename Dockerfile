FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /Ocr
WORKDIR /Ocr/
RUN apt update && apt install tesseract-ocr -y && apt install libtesseract-dev -y
RUN pip install --upgrade pip setuptools wheel
COPY requirements.txt /Ocr/
RUN pip install -r requirements.txt
RUN apt-get update ##[edited]
RUN apt-get install 'ffmpeg'\
    'libsm6'\ 
    'libxext6'  -y
COPY . /Ocr/