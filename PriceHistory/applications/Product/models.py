from django.db import models
from datetime import date

from ..Core.models import Shop
from ..Category.models import Subcategory


class ProcessedProduct(models.Model):
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(unique=True)
    translit_name = models.CharField(unique=True)
    image_path = models.ImageField(upload_to='ProcessedProduct/', null=True, blank=True)
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    unit = models.CharField(max_length=16, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    composition = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=64, null=True, blank=True)
    calories = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    carbohydrates = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    fats = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    proteins = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.name} | {self.subcategory}'

    class Meta:
        db_table = 'processed_product'


class RawProduct(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    raw_category = models.CharField(null=True, blank=True)
    raw_subcategory = models.CharField(null=True, blank=True)
    raw_name = models.CharField()
    processed_product = models.ForeignKey(ProcessedProduct, on_delete=models.SET_NULL, null=True, blank=True)
    url = models.URLField(unique=True)
    image_path = models.ImageField(upload_to='RawProduct/', null=True, blank=True)
    raw_weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    raw_unit = models.CharField(max_length=16, null=True, blank=True)
    raw_description = models.TextField(null=True, blank=True)
    raw_composition = models.TextField(null=True, blank=True)
    raw_country = models.CharField(max_length=64, null=True, blank=True)
    raw_calories = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    raw_carbohydrates = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    raw_fats = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    raw_proteins = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.raw_name}'

    class Meta:
        db_table = 'raw_product'


class ProductHistoryRecord(models.Model):
    raw_product = models.ForeignKey(RawProduct, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField(default=date.today)

    def __str__(self):
        return f'{self.raw_product} | {self.price} | {self.date}'

    class Meta:
        db_table = 'product_history-record'
