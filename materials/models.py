from django.conf import settings
from django.db import models

from product.models import NULLABLE


class Material(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(upload_to='materials/', verbose_name='Изображение', null=True, blank=True)
    slug = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_publish = models.BooleanField(default=False, verbose_name='Публикация')
    views_count = models.IntegerField(default=0, verbose_name='Просмотры')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='user', **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'
