from django.urls import path

from .views import all_products_view, product_detail, search_view

app_name = "shope"

urlpatterns = [
    path("", all_products_view, name="all_products"),
    path("search/", search_view, name="search"), # must be above slug
    path("<slug:category_slug>/", all_products_view, name="all_products_by_category"),
    path("book/<slug:slug>/", product_detail, name="product_detail"),
]
