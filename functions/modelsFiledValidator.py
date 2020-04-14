from django.db import models


class PercentageField(models.FloatField):
    description = "A field to save percentage in db"

    def __init__(self, *args, **kwargs):
        super(PercentageField, self).__init__(*args, **kwargs)

    # Convert content of database to python objects
    def to_python(self, value):
        if not value:
            val = 0
        if isinstance(value, str):
            val = value.replace("%", "")
            if is_number(val):
                return val/100
            else:
                return 0
        return val

    # Save python objects into database, for 'objects.create'
    def get_prep_value(self, value):
        if value is None:
            return value
        val = str(value*100)
        return str(val + "%")

    # Convert python objects to string, for objects.get
    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_db_prep_value(value, None)


def is_number(s):
    if s is None:
        return False
    try:
        float(s)
        return True
    except ValueError:
        return False
