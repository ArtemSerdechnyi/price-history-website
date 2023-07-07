from django.db import models
from ..Core.models import Shop


class Category(models.Model):
    category_name = models.CharField(unique=True)

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = 'category'
        ordering = ['category_name']


class Subcategory(models.Model):
    subcategory = models.CharField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category} --> {self.subcategory}'

    class Meta:
        db_table = 'subcategory'
        ordering = ['category__category_name', 'subcategory']


class RawSubcategory(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    url = models.URLField(unique=True, primary_key=True)
    subcategory = models.ManyToManyField(Subcategory)

    def __str__(self):
        return f'{self.subcategory} | {self.url}'

    class Meta:
        db_table = 'raw_subcategory'
