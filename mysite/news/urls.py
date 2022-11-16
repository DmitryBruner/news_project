from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page
urlpatterns = [
    #path('', index, name='home'),
    path('', HomeNews.as_view(), name='home'),
#    path('', cache_page(60)(HomeNews.as_view()), name='home'),  кэш страницы на 60 секунд
    #path('category/<int:category_id>/', get_category, name='category'),
    path('category/<int:category_id>/', HewsByCategory.as_view(), name='category'),
    #path('news/<int:news_id>/', view_news, name='view_news'),
    path('news/<int:pk>/', ViewNews.as_view(), name='view_news'),
    path('news/add_news/', CreateNews.as_view(), name='add_news'),
    #path('news/add_news/', add_news, name='add_news'),
    path('contacts/', my_mail_send, name='contacts'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),

]

