from django.db import models

# Create your models here.


class RequestLog(models.Model):
    path = models.CharField(max_length=255)
    is_latest = models.BooleanField(default=True)
