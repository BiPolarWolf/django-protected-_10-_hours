from django.contrib import admin
from django.http.request import HttpRequest
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')
    ordering = ('name',)
    
    def get_prepopulated_fields(self, request,obj=None):
        return {'slug': ('name',) }
    


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','brand', 'slug', 'price', 'category','create_at','update_at', 'available')
    list_filter = ('available', 'create_at', 'update_at', 'category')   
    ordering = ('title',)
    
    def get_prepopulated_fields(self, request,obj=None):
        return {'slug': ('title',) }