# OCR VALIDATION PROJECT

## Setup Steps

### Virtual Enviroment

Create virtual enviroment for Python

```
python -m venv C:\path\to\your\project
```

Activate virtual enviroment (Windows)

```
.\venv\Scripts\activate
```

### Install And Set Up Django

```
pip install Django
```

Crate django project

```
django-admin startproject Ocr_app
```

Create pages app

```
python manage.py startapp pages
```

Create listings app

```
python manage.py startapp listings
```

Create validation app

```
python manage.py startapp validation
```

Add created app to installed app list
```
INSTALLED_APPS = [
    # Add pages apps, listings apps, validation apps
    'pages.apps.PagesConfig',
    'listings.apps.ListingsConfig',
    'validation.apps.ValidationConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

Collect static files (Save static files in Ocr_app including css, img, js, webfonts etc..)

```
python manage.py collectstatic
```

### MongoDB with Django

Install mongodb module for django

```
pip install djongo
```

Go to the settings.py file of Ocr_app

```
# If your database is in your local machine
DATABASES = {
   ‘default’: {
      ‘ENGINE’: ‘djongo’,
      ‘NAME’: ‘your-db-name’,
   }
}
```

```
# If your database is on any server
DATABASES = {
   ‘default’: {
      ‘ENGINE’ : ‘djongo’,
      
       ‘NAME’ : ‘your-db-name’, #as named on server
      
       'HOST' : 'mongodb://<dbuser>:<dbpassword>@ds259144.mlab.com:59144/<db-name>',
# that is your connection link with your username,password and db name,here i created a db using mlabs of mongodb
       'USER' : '<dbuser>',
       'PASSWORD' : '<dbpassword>',

   }
}
```

Create databases migrations
```
python manage.py migrate
```

After create models for Listings and Validations, make a migrations to database
```
python manage.py makemigrations
```
```
python manage.py migrate
```

Manage Media folder with [link to tutorial](https://djangocentral.com/managing-media-files-in-django/)


## Start the Django app

Start server

```
python manage.py runserver
```