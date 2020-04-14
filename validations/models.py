from django.db import models
from ocrfiles.models import Ocrfiles
from functions.modelsFiledValidator import PercentageField


class Validation(models.Model):
    ocrfiles = models.ForeignKey(
        Ocrfiles, related_name='validations', on_delete=models.CASCADE)
    page_number = models.IntegerField(default=1)
    get_text = models.CharField(max_length=200)
    startX = models.FloatField(default=0)
    endX = models.FloatField(default=0)
    startY = models.FloatField(default=0)
    endY = models.FloatField(default=0)
    correction_rate = PercentageField(default=0)
    is_correct = models.BooleanField(default=False)
    feedback_text = models.CharField(max_length=200, blank=True)
    is_exist = models.BooleanField(default=False)

    def __str__(self):
        return self.get_text
