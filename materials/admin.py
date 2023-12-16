from django.contrib import admin

from materials.models import Material


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    fields = ('title', 'body', 'image',)
    list_display = ('title',)
