from django.contrib import admin
from .models import Products

class ProductsAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')  # Укажите поля, которые хотите видеть в списке
    search_fields = ('title',)  # Поля для поиска

admin.site.register(Products, ProductsAdmin)  # Регистрация модели
