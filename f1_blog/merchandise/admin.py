from django.contrib import admin

from f1_blog.merchandise.models import Category, Merchandise


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name',]


@admin.register(Merchandise)
class MerchandiseAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'price', 'category',]
