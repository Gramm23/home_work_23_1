from django.contrib import admin

from product.models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ['title', 'price', 'description', 'image', 'category', 'active']
    list_display = ['title', 'price', 'category', 'image', ]
    list_filter = ['category', ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['product_name', ]
    list_display = ['product_name', ]


@admin.register(Version)
class Version(admin.ModelAdmin):
    fields = ['version_name', 'version_number', 'active', 'product', ]
    list_display = ['version_name', ]
