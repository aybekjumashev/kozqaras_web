# config/urls.py
from django.contrib import admin
from django.urls import path, include # include funkciyasın import etiwdi umıtpań
from django.conf import settings       # settings import etiw
from django.conf.urls.static import static # static funkciyasın import etiw

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('articles.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')), # <-- CKEditor júklew URL'leri
    # ...
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    #urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Statik fayllar ushın (eger kerek bolsa)