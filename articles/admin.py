# articles/admin.py
from django.contrib import admin
from .models import Article, Category, Author

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'website') # Kórsetiletuǵın baganalar
    search_fields = ('full_name', 'email', 'bio') # Izlew maydanları
    prepopulated_fields = {'slug': ('full_name',)} # Atama jazılǵanda slug avtomat toltırıladı

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_categories', 'published_date', 'created_at', 'updated_at') # 'category' ornına 'display_categories'
    list_filter = ('published_date', 'categories') # 'category' ornına 'categories'
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    # filter_horizontal = ('categories',) # <-- Jaqsıraq interfeys ushın
    filter_vertical = ('categories',) # <-- filter_horizontal ǵa alternativ (vertikal kórinis)
    raw_id_fields = ('author',)
    readonly_fields = ('view_count',) # Redaktorlaw betinde kórsetiw ushın (eger kerek bolsa)

    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()[:3]]) + ('...' if obj.categories.count() > 3 else '')
    display_categories.short_description = 'Kategoriyalar'