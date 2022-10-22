from django import forms
from .models import Category

class NewsForm(forms.Form):
    title = forms.CharField(max_length=150, label='Название')
    content = forms.CharField(label='Текст', required=False)
    is_published = forms.BooleanField(label='Опубликовано', initial=True)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Катеригия', empty_label='Выберете категорию')