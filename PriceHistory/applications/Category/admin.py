from django.contrib import admin

from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'subcategory')
    list_display_links = ('subcategory',)
    list_filter = ('category__category_name',)


class RawSubcategoryListFilter(admin.SimpleListFilter):
    title = 'Subcategory'
    parameter_name = 'subcategory'

    def lookups(self, request, model_admin):
        categories = Category.objects.all()
        for category in categories:
            subcategories = Subcategory.objects.filter(category=category)
            yield str(category.id), str(category.category_name)
            for subcategory in subcategories:
                yield str(subcategory.id), f' - {subcategory.subcategory}'

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(subcategory=self.value())
        return queryset


@admin.register(RawSubcategory)
class RawSubcategoryAdmin(admin.ModelAdmin):
    list_display = ('shop', 'url')
    list_display_links = ('url',)
    # list_filter = ('subcategory__subcategory', 'subcategory__category__category_name')
    list_filter = (RawSubcategoryListFilter,)
    search_fields = ('subcategory__subcategory',)
    search_help_text = 'Subcategory name'
