from django.db import models

# Create your models here.
class Currency(models.Model):
    symbol = models.CharField(max_length=100)
    
    def __str__(self):
        return self.symbol