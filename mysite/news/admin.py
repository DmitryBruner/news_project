from django.contrib import admin
from .models import News, Category

class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'title', 'created_at', 'updated_at', 'is_published')
    list_display_links = ('id', 'title') #делаю оба поля ссылками на редактирование новости
    search_fields = ('title', 'content') #поля для поиска в админке
    list_editable = ('category', 'is_published')
    list_filter = ('category', 'is_published')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title') #делаю оба поля ссылками на редактирование категории
    search_fields = ('title',) #поле для поиска в админке #тут кортеж поэтому запятая в конце

admin.site.register(News, NewsAdmin)  #порядок важен сначала регистрируем основную модель а после класс настройки этой модели
admin.site.register(Category, CategoryAdmin)