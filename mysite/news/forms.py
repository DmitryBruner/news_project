from django import forms
from .models import Category

class NewsForm(forms.Form):
    title = forms.CharField(max_length=150, label='Название', widget=forms.TextInput(attrs={'class': 'form-control'})) #тут мы подключаем определенный виджет поля и шаблон класса из бустрапа чтобы изменить внешний вид поля
    content = forms.CharField(label='Текст', required=False, widget=forms.Textarea(attrs={'rows': 5,'class': 'form-control'}))
    is_published = forms.BooleanField(label='Опубликовано', initial=True)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label='Выберете категорию', widget=forms.Select(attrs={'class': 'form-control'}))