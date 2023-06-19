from django.db import models
from dataspace.models import OS

# Create your models here.

class train_data(models.Model):
    L1_I = models.FloatField()
    L1_D = models.FloatField()
    L2 = models.FloatField()
    L3 = models.FloatField()
    Max_Hz = models.FloatField()
    OS = models.ForeignKey(OS, on_delete=models.CASCADE)
    Memory = models.FloatField()
    Base_Pointers = models.FloatField()
    Peak_Pointers = models.FloatField()
    nominal = models.FloatField()
    cores = models.IntegerField()
