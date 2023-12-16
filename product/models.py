from django.db import models

NULLABLE = {
    'null': True,
    'blank': True
}


class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to="images/", verbose_name="Изображение")
    price = models.IntegerField(verbose_name="Стоимость")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения"
    )
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, verbose_name="Категория"
    )

    active = models.BooleanField(default=True, verbose_name="Наличие")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Category(models.Model):
    product_name = models.CharField(max_length=150, verbose_name="Категория")
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Version(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="продукт",
        related_name="versions",
    )
    version_number = models.FloatField(verbose_name="версия продукта")
    version_name = models.CharField(max_length=50, verbose_name="название версии")
    active = models.BooleanField(default=False, verbose_name="активная")

    def __str__(self):
        return f"{self.version_name}"

    class Meta:
        verbose_name = "версия"
        verbose_name_plural = "версии"
