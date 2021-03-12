from django.db import models


# Create your models here.

class Review(models.Model):
    menu = models.TextField()
    comment = models.TextField()
    rating = models.IntegerField()
    time = models.TextField()

    class Meta:
        db_table = "Reviews"
