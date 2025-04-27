# articles/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from django.db.models import Q, F
from .utils import normalize_text

def home(request):
    return redirect('article_list')


def search_results(request):
    """Maqalalardı atama hám mazmun boyınsha izlew nátiyjelerin kórsetedi."""
    query_original = request.GET.get('q', '')
    results = []

    if query_original:
        query_normalized = normalize_text(query_original) # Sorawdı da normalizaciyalaw

        results = Article.objects.filter(
            Q(title_normalized__icontains=query_normalized) | Q(content_normalized__icontains=query_normalized),
            published_date__lte=timezone.now()
        ).order_by('-published_date') # distinct endi kerek emes

    # Izlew nátiyjelerin betlew (pagination)
    paginator = Paginator(results, 5) # Hár bette 5 nátiyje
    page_number = request.GET.get('page', 1)
    try:
        results_page = paginator.page(page_number)
    except PageNotAnInteger:
        results_page = paginator.page(1)
    except EmptyPage:
        results_page = paginator.page(paginator.num_pages)

    context = {
        'query': query_original,         # Izlew sorawın shablonǵa jiberiw
        'articles': results_page, # Betlengen nátiyjelerdi 'articles' dep jiberiw (article_list shablonı menen sáykeslik ushın)
        'page_obj': results_page, # Betlew ushın Page obiektı
        'paginator': paginator,
        'is_search': True,      # Bul izlew beti ekenligin kórsetiwshi belgı (shablonda paydalı bolıwı múmkin)
    }
    # Biz izlew nátiyjelerin kórsetiw ushın bar article_list.html shablonın qayta qollanamız
    return render(request, 'articles/article_list.html', context)

def article_list(request, category_slug=None): # category_slug parametrın qosıw
    """Baspa etilgen maqalalardı kórsetedi, múmkin kategoriya boyınsha filtrlep."""
    category = None
    object_list = Article.objects.filter(published_date__lte=timezone.now())

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        object_list = object_list.filter(categories=category)

    paginator = Paginator(object_list.order_by('-published_date'), 10)
    page_number = request.GET.get('page', 1)

    try:
        articles = paginator.page(page_number)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    context = {
        'articles': articles,
        'page_obj': articles,
        'paginator': paginator,
        'category': category, # Házirgi kategoriyanı shablonǵa jiberiw
    }
    return render(request, 'articles/article_list.html', context)


def article_detail(request, slug):
    """Bir maqalaniń detaların kórsetedi hám kóriwler sanın asıradı."""
    article = get_object_or_404(Article, slug=slug, published_date__lte=timezone.now())

    # <<< KÓRIWLER SANÍN ASÍRÍW >>>
    # F() arqalı bazada atomik (bólinbeytuǵın) túrde +1 operaciyasın orınlaw
    article.view_count = F('view_count') + 1
    article.save(update_fields=['view_count']) # Tek usı maydandı jańalaw
    # <<< ASÍRÍW AQIRI >>>

    # Maqalani jańalanǵan mánis penen qayta júklew (kontekstke durıs san barıwı ushın)
    article.refresh_from_db()

    full_image_url = None
    if article.featured_image:
        full_image_url = request.build_absolute_uri(article.featured_image.url)

    context = {
        'article': article,
        'full_image_url': full_image_url,        
        }
    return render(request, 'articles/article_detail.html', context)

# timezone import etiwdi umıtpań
from django.utils import timezone