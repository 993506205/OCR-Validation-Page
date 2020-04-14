from django.db import models
from datetime import datetime

class DirProject(models.Model):
    name = models.CharField(max_length=50)
    creator_id = models.IntegerField(default=0)
    date = models.DateField(default=datetime.now, blank=True)
    description = models.TextField()
    
    def __str__(self):
        return self.name