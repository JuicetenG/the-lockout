from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Gear(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=150)
    type = models.CharField(max_length=100)
    cost = models.IntegerField()
    trade = models.BooleanField()
    image = models.URLField(max_length=500, blank=True, null=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.make} {self.model} {self.type}"
    


