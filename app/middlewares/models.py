from django.db import models

# Create your models here.


class RequestLog(models.Model):
    path = models.CharField(max_length=255)
    include_for_count = models.BooleanField(default=True)
