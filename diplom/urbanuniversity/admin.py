from django.contrib import admin
from .models import Products

class ProductsAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')  # Поля для отображения
    search_fields = ('title',)  # Поля для поиска
    list_filter = ('price',)  # Поля для фильтрации
    list_editable = ('price',)  # Поля для редактирования
    exclude = ('image',)  # Исключаем поле изображения


admin.site.register(Products, ProductsAdmin)  # Регистрация модели
