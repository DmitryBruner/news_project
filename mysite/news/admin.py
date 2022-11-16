from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import News, Category
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = News
        fields = '__all__'
class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = ('id', 'category', 'title', 'created_at', 'updated_at', 'is_published', 'get_photo')
    list_display_links = ('id', 'title') #делаю оба поля ссылками на редактирование новости
    search_fields = ('title', 'content') #поля для поиска в админке
    list_editable = ('category', 'is_published')
    list_filter = ('category', 'is_published')
    fields = ('title', 'category', 'content', 'photo', 'get_photo', 'is_published', 'views', 'created_at', 'updated_at')
    readonly_fields = ('get_photo', 'views', 'created_at', 'updated_at')
    save_on_top = True #добавляет снизу панель сохранения 
    def get_photo(self, obj):
        """показать фото в админке не ссылкой а картинкой"""
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')
        else:
            return 'фото не установлено'
    get_photo.short_description = 'Миниатюра' #меняет название в фильтрах админки
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title') #делаю оба поля ссылками на редактирование категории
    search_fields = ('title',) #поле для поиска в админке #тут кортеж поэтому запятая в конце

admin.site.register(News, NewsAdmin)  #порядок важен сначала регистрируем основную модель а после класс настройки этой модели
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Управление новостями'
admin.site.site_header = 'Управление новостями'