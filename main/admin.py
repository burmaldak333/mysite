from django.contrib import admin
from .models import Section, Block

class BlockInline(admin.TabularInline):
    """Позволяет добавлять и редактировать блоки прямо со страницы Раздела"""
    model = Block
    extra = 1  # Количество пустых полей для новых блоков по умолчанию
    fields = ['title', 'content', 'image', 'position']


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'position']
    prepopulated_fields = {'slug': ('title',)}  # Автоматически генерирует slug из названия
    inlines = [BlockInline]  # Встраиваем блоки в админку раздела


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'position', 'created_at']
    list_filter = ['section']