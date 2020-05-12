# OCR VALIDATION PROJECT

This is a OCR validation web page project as my thesis project.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Creating VIRTUAL ENVIROMENT
Run [startup.sh](startup.sh) for creating virtualenv and installing needed modules.

### RUN SERVER
On Windows, it is needed to activate your virtualenv first.
```
.env/Scripts/activate
```
Start your server
```
python manage.py runserver
```

### BROWSE LOCALHOST (IE > 8.0)
```
http://127.0.0.1:8000/
```

## Create superuser for django project
```
python manage.py createsuperuser
```
