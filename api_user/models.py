from django.db import models


class Review(models.Model):
    menu = models.TextField()
    comment = models.TextField()
    rating = models.IntegerField()
    time = models.TextField()

    class Meta:
        db_table = "Review"


class Summary(models.Model):
    word = models.TextField()

    class Meta:
        db_table = "Summary"
