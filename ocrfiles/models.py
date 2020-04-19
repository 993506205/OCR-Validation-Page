from datetime import datetime
from django.db import models
from dirprojects.models import DirProject

class Ocrfiles(models.Model):
    dir_project = models.ForeignKey(DirProject, related_name="ocrfiles", on_delete=models.CASCADE)
    file_name = models.CharField(max_length=250)
    file_extension = models.CharField(max_length=250)
    upload_date = models.DateField(default=datetime.now, blank=True)
    file_size = models.FloatField()

    scanned_file = models.FileField(
        upload_to='Ocr_files/Ocr_Scanned_files/%Y/%m/', null=True)

    def __str__(self):
        return self.file_name


class OcrConvertedImage(models.Model):
    image_name = models.CharField(max_length=250, default='')
    page_number = models.IntegerField(default=0)
    ocrfiles = models.ForeignKey(
        Ocrfiles, related_name='converted_image', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='Ocr_files/Ocr_Converted_files/%Y/%m/', null=True)
    
    textRegion_image = models.FileField(
        upload_to='Ocr_files/Ocr_TextRegion_images/%Y/%m/', null=True
    )

    def __str__(self):
        return self.image_name
