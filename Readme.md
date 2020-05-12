# OCR VALIDATION PROJECT

This is a OCR validation web page project as my thesis project.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

## Requirements

This thesis project requires:

* [Docker](https://www.docker.com/get-started)

## Installation

Setup the project using following command,

```
docker-compose up --build -d
```
### Store MongoDB data

The Database is only saved in container, inside `/data/da`. Shut dwon the MongoDB `mongo` services will clean all the data.

### Django database migration automatically at beginning.

The services `make-migration` amd `migration` runs after setting up the database when `docker up` the project.

### Django Web Project

The main page of the thesis project is at [http://localhost:8000/].

### MongoDB admin interface

This project contains a web-base interface for MongoDB which is [mongo-express](http://github.com/mongo-express/mongo-express) at port 8081.

## Functions of the Project

### Create a user account

User needs to create an account for using the validation functions.

### Create a Directory Project Folder for files

Click the `Create` button on home page and select the files for Recognition.

### Click the file for recognition

In `OCR FILES LISTING` page, click image's name link under image for OCR validation. User can fix the Wrong OCR text fields in `Validation` text listing (There will be Parameters Correction for training tesseract in the future).

## Reference

This Dockerlization method is learning from [balanpradeepkumar's github](https://github.com/balanpradeepkumar/docker_django_mongodb).