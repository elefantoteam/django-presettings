from utils.base_models import BaseModel
from django.db import models

# Create your models here.
class JustModel(BaseModel):
    name = models.CharField(max_length=20)