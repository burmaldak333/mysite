from django.db import models


class Section(models.Model):
    """Модель раздела сайта"""
    title = models.CharField(max_length=200, verbose_name="Название раздела")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL-алиас (slug)")
    position = models.PositiveIntegerField(default=0, verbose_name="Порядковый номер при выводе")

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"
        ordering = ['position']  # Сортировка по позиции по умолчанию

    def __str__(self):
        return self.title


class Block(models.Model):
    """Модель блока с содержимым внутри раздела"""
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name='blocks',
        verbose_name="Раздел"
    )
    title = models.CharField(max_length=200, verbose_name="Заголовок блока", blank=True)
    content = models.TextField(verbose_name="Содержимое (текст/HTML)")
    image = models.ImageField(upload_to='blocks/', blank=True, null=True, verbose_name="Изображение")
    position = models.PositiveIntegerField(default=0, verbose_name="Порядковый номер внутри раздела")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Блок контента"
        verbose_name_plural = "Блоки контента"
        ordering = ['position']

    def __str__(self):
        return self.title or f"Блок {self.id} в разделе {self.section.title}"