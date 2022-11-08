from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView

from .models import News, Category
from .forms import NewsForm

#class HomeNews(ListView):
#    model = News   эта конструкция выводит то же что и функция index для выводв в шаблоне нужно использовать object_list

class HomeNews(ListView):
    """Вывод главной страницы сайта"""
    model = News
    template_name = 'news/home_news_list.html' #переопределение шаблона по умолчанию
    context_object_name = 'news' #переопределение базового списка для вывода в свой класс (дефолтный объект)
    #extra_context = {'title': 'Главная'} #используется только для статичных данных

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs) #наследовали атрибуты от шаблона
        context['title'] = 'Главная страница' #переопределили title
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True) #фильтр по опубликовано
# def index(request):
#     news = News.objects.order_by('-created_at')
#     context = {'news': news,
#                'title': 'Список новостей'
#                }
#     return render(request, 'news/index.html', context)
class HewsByCategory(ListView):
    """Вывод страницы по категории"""
    model = News
    template_name = 'news/home_news_list.html' #переопределение шаблона по умолчанию
    context_object_name = 'news' #переопределение базового списка для вывода в свой класс (дефолтный объект)
    allow_empty = False #неразрешаем показ пустых списокв вместо 500 ошибка будет 404

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs) #наследовали атрибуты от шаблона
        context['title'] = Category.objects.get(pk=self.kwargs['category_id']) #переопределили title для каждой категории
        return context

    def get_queryset(self):

        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True) #фильтр по опубликовано


# def get_category(request, category_id):
#     """вывод категорий с помощью функции"""
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#
#     return render(request, 'news/category.html', {'news': news,
#                                                   'category': category})


class ViewNews(DetailView):
    """Вывод отдельной новости"""
    model = News
    #template_name = 'news/news_view_news.html'  # переопределение шаблона по умолчанию
    #pk_url_kwarg = 'news_id'  указание откуда брать id
    context_object_name = 'news_item'

class CreateNews(CreateView):
    """Добавление новости"""
    form_class = NewsForm
    template_name = 'news/add_news.html'
    #если в моделе прописан метод гет абсолюте юрл то будет редирект на только что созданный объект




# def view_news(request, news_id):
#     """Вывод отдельной новости"""
#     news_item = get_object_or_404(News, pk=news_id)
#     #news_item = News.objects.get(pk=news_id)
#     return render(request, 'news/view_news.html', {'news_item': news_item})


# def add_news(request):
#       """Добавление новости"""
#     if request.method == "POST":
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             news = form.save()
#             #не связанная с моделью форма. логика сохраненния
#             #print(form.cleaned_data) сюда попадает словарь из формы и его можно посмотреть. данные в него попадают после валидации
#             #news = News.objects.create(**form.cleaned_data) #распаковка словарей**.
#             #return redirect(news)   #это редирект на только что созданную новость
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})