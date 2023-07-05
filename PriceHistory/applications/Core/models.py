from django.db import models


class Shop(models.Model):
    name = models.CharField(max_length=32, unique=True)
    url = models.URLField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'shop'
