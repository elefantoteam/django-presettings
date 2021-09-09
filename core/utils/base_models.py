from django.db import models
from rest_framework import serializers
from unixtimestampfield.fields import UnixTimeStampField

class BaseModel(models.Model):
    created_at = UnixTimeStampField(auto_now_add=True)
    updated_at = UnixTimeStampField(auto_now=True)

    class Meta:
        abstract = True