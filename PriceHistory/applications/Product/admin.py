from django.contrib import admin

from .models import *

admin.site.register(RawProduct)
admin.site.register(ProcessedProduct)
admin.site.register(ProductHistoryRecord)
