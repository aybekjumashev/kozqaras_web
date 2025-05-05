# articles/urls.py
from django.urls import path
from . import views # Sol papkadaǵı views.py faylın import etiw

urlpatterns = [
    path('maqalalar/izlew/', views.search_results, name='search_results'),
    path('maqalalar/', views.article_list, name='article_list'), # /articles/ ushın
    path('', views.home_page, name='home'), 
    path('maqalalar/kategoriya/<slug:category_slug>/', views.article_list, name='articles_by_category'),
    path('maqalalar/<slug:slug>/', views.article_detail, name='article_detail'), # /articles/mening-maqalam/ ushın
]