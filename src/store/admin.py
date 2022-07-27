from django.contrib import admin
from django.contrib.sessions.models import Session
from .models import Category, Product


admin.site.register(Session)


@admin.register(Category)
class CateogryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', )
    readonly_fields = ("slug", "created", "updated")
    date_hierarchy = "created"
    # prepopulated_fields = {"slug": ("name", )}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'price', 'in_stock',
                    'is_active')
    list_filter =  ("in_stock", "is_active")
    list_editable = ("price", "in_stock", "is_active")
    # prepopulated_fields = {"slug": ("title", )}
    date_hierarchy = "created"
    readonly_fields = ("slug", "created", "updated")
