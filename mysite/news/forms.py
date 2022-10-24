from django import forms
#from .models import Category
from .models import News
import re
from django.core.exceptions import ValidationError


#class NewsForm(forms.Form):
    #"""форма не связанная с моделью. тут нарушение dry тк мы дублируем код с моделью"""
    #title = forms.CharField(max_length=150, label='Название', widget=forms.TextInput(attrs={'class': 'form-control'})) #тут мы подключаем определенный виджет поля и шаблон класса из бустрапа чтобы изменить внешний вид поля
    #content = forms.CharField(label='Текст', required=False, widget=forms.Textarea(attrs={'rows': 5,'class': 'form-control'}))
    #is_published = forms.BooleanField(label='Опубликовано', initial=True)
    #category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label='Выберете категорию', widget=forms.Select(attrs={'class': 'form-control'}))

class NewsForm(forms.ModelForm):
    """форма связанная с моделью"""
    class Meta:
        model = News
        #fields = '__all__' вытащить все поля в соответствующем формате
        fields = {'title', 'content',  'category', 'is_published'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            #'is_published': forms.CheckboxInput()
        }

    def clean_title(self):
        """кастомные валидаторы"""
        title = self.cleaned_data['title']
        if re.match(r'\d', title): #регулярка
            raise ValidationError('Название не должно начинаться с цифры')
        return title