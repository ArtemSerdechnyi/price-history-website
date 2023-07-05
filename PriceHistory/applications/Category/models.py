from django.db import models


class Category(models.Model):
    category_name = models.CharField(unique=True)

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = 'category'


class Subcategory(models.Model):
    subcategory_name = models.CharField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category} --> {self.subcategory_name}'

    class Meta:
        db_table = 'subcategory'
