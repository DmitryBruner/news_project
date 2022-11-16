from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView

from django.contrib import messages

from django.core.mail import send_mail
from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from .util import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.core.paginator import Paginator
#class HomeNews(ListView):
#    model = News   эта конструкция выводит то же что и функция index для выводв в шаблоне нужно использовать object_list


def my_mail_send(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'bruner.expert@yandex.ru', ['bruner.expert@gmail.com'], fail_silently=True) #если в фолс то выдается ошибка в коде если тру то ошибка общая для юзера fail_silently=True
            if mail:
                messages.success(request, 'Пимьмо успешно отправлено!')
                return redirect('contacts')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка валидации!')
    else:
        form = ContactForm()

    return render(request, 'news/contacts.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации!')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')


class HomeNews(MyMixin, ListView):
    """Вывод главной страницы сайта"""
    model = News
    template_name = 'news/home_news_list.html' #переопределение шаблона по умолчанию
    context_object_name = 'news' #переопределение базового списка для вывода в свой класс (дефолтный объект)
    #extra_context = {'title': 'Главная'} #используется только для статичных данных
    queryset = News.objects.select_related('category')
    #mixin_prop = 'hello world' # пример использования миксинов
    paginate_by = 2
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs) #наследовали атрибуты от шаблона
        context['title'] = self.get_upper('Главная страница') #переопределили title
        context['mixin_prop'] = self.get_prop()
        return context

#     def get_queryset(self):
#         return News.objects.filter(is_published=True).select_related('category') #фильтр по опубликовано также использование жадных sql запросов (грубо говоря джоиним единичные запросы)
#  def index(request):
#     news = News.objects.order_by('-created_at')
#     context = {'news': news,
#                'title': 'Список новостей'
#                }
#     return render(request, 'news/index.html', context)
class HewsByCategory(ListView):
    """Вывод страницы по категории"""
    model = News
    template_name = 'news/category.html' #переопределение шаблона по умолчанию
    context_object_name = 'news' #переопределение базового списка для вывода в свой класс (дефолтный объект)
    allow_empty = False #неразрешаем показ пустых списокв вместо 500 ошибка будет 404
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs) #наследовали атрибуты от шаблона
        context['title'] = Category.objects.get(pk=self.kwargs['category_id']) #переопределили title для каждой категории
        return context

    def get_queryset(self):

        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category') #фильтр по опубликовано также использование жадных sql запросов (грубо говоря джоиним единичные запросы)


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


class CreateNews(LoginRequiredMixin, CreateView):
    """Добавление новости"""
    form_class = NewsForm
    template_name = 'news/add_news.html'
    #если в моделе прописан метод гет абсолюте юрл то будет редирект на только что созданный объект
    login_url = '/admin/' #перенаправляет на форму регистрации если незареганный пользователь пытается зайти на страницу ему недоступную по прямой ссылке можно вместо этого просто не давать доступ к странице



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