# articles/models.py
from django.db import models
from django.utils import timezone
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from .utils import normalize_text
from bs4 import BeautifulSoup 

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Kategoriya Atı")
    slug = models.SlugField(max_length=110, unique=True, verbose_name="Silteme (slug)")

    class Meta:
        ordering = ['name']
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('articles_by_category', kwargs={'category_slug': self.slug})


class Author(models.Model):
    full_name = models.CharField(max_length=150, verbose_name="Tolıq Atı (AÁÁ)")
    slug = models.SlugField(max_length=160, unique=True, verbose_name="Silteme (slug)")
    profile_picture = models.ImageField(
        upload_to='author_pics/',
        blank=True,
        null=True,
        verbose_name="Profil Súwreti"
    )
    bio = models.TextField(blank=True, verbose_name="Biografiya/Haqqında")
    email = models.EmailField(blank=True, verbose_name="Elektron Pochta")
    website = models.URLField(blank=True, verbose_name="Web-sayt")

    class Meta:
        ordering = ['full_name']
        verbose_name = "Avtor"
        verbose_name_plural = "Avtorlar"

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        # Keleshekte avtor profili betin jaratsaq, usı URL kerek boladı
        # Házirshe # yamasa bas betke jiberip turamız
        # return reverse('author_profile', kwargs={'author_slug': self.slug})
        return "#" # Yamasa reverse('article_list')

class Article(models.Model):
    categories = models.ManyToManyField(
        Category,
        blank=True, # Admin panelinde bos qaldırıw múmkin
        related_name='articles', # Kategoriya obiektinen maqalalarǵa ótiw (category.articles.all())
        verbose_name="Kategoriyalar" # Kóplik formada atama
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL, # Avtor óshirilse, maqalada avtor maydanı bos qaladı
        null=True,  # Bazada bos bolıwı múmkin
        blank=True, # Admin panelinde májbúriy emes
        related_name='articles', # Avtor obiektinen maqalalarǵa ótiw (author.articles.all())
        verbose_name="Avtor"
    )
    title = models.CharField(max_length=250, verbose_name="Ataması")
    slug = models.SlugField(max_length=250, unique=True, verbose_name="Silteme (slug)")
    content = RichTextUploadingField(verbose_name="Mazmunı")
    title_normalized = models.CharField(max_length=250, blank=True, editable=False, db_index=True) # Izlew ushın
    content_normalized = models.TextField(blank=True, editable=False) # Izlew ushın
    featured_image = models.ImageField(
        upload_to='article_images/',
        blank=True,
        null=True,
        verbose_name="Tiykarǵı Súwret"
    )
    published_date = models.DateTimeField(default=timezone.now, verbose_name="Baspa etilgen sáne")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Jaratılǵan sáne")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Jańalanǵan sáne")

    view_count = models.PositiveIntegerField(
        default=0,                 # Baslanǵısh mánisi 0
        editable=False,            # Admin panelinde tikkeley ózgertiw múmkin emes
        verbose_name="Kóriwler Sanı"
    )

    telegram_post_url = models.URLField(
        max_length=500,  # URL uzın bolıwı múmkin
        blank=True,      # Májbúriy emes
        null=True,       # Bazada bos bolıwı múmkin
        verbose_name="Telegram Pikir URL",
        help_text="Pikirlerdi jalǵaw ushın qollanılǵan Telegram postınıń tolıq siltemesi (https://...). Bos qaldırılsa, pikirler bólimi kórsetilmeydi."
    )

    class Meta:
        ordering = ['-published_date']
        verbose_name = "Maqala"
        verbose_name_plural = "Maqalalar"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        self.title_normalized = normalize_text(self.title)
        
        if self.content:
           soup = BeautifulSoup(self.content, 'html.parser')
           plain_content = soup.get_text()
           self.content_normalized = normalize_text(plain_content)
        else:
           self.content_normalized = ""

        super().save(*args, **kwargs) # Original save metodın shaqırıw