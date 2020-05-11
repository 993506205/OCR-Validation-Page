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

## USERS AND ADMIN

### CREATE SUPERUSER FOR DJANGO PROJECT
```
python manage.py createsuperuser
```
### CHECK ADMIN PAGE
```
http://127.0.0.1:8000/admin/
```
### CREATE USER BY CLICK REGISTER BUTTON

## CREATE DIRECTORY PROJECT FOR FILES
Click **CREATE** button in home page (NEED TO LOGIN) for creating OCR files directory project.

In **OCR FILES LISTING**, check your files. Files' name will link to Validation page.

In **Dashboard**, you can update directory project with name and description and delete it.


