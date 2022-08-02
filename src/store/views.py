from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from .models import Category, Product

# def all_categories(request):
#     categories = get_list_or_404(Category)
#     context = {
#         "categories": categories
#     }
#     return render(request, )




def all_products_view(request, category_slug=None):
    # try:
    #     products = Product.objects.filter(in_stock=True, is_active=True)
    # except Product.DoesNotExist:
    #     raise Http404
    try:
        products = Product.products.all()
    except Product.DoesNotExist:
        raise Http404
    category_obj = None
    all_products = True
    if category_slug is not None:
        all_products = False
        category_obj = get_object_or_404(Category, slug=category_slug)
        # Category.get_products_by_category(category_obj)
        # products = get_list_or_404(Product,
        #                            category=category_obj,
        #                            in_stock=True,
        #                            is_active=True)
        products = Product.objects.filter(
            category=category_obj,
            in_stock=True,
            is_active=True
        )
    context = {
        "all_products": all_products,
        "category": category_obj,
        "products": products
    }
    return render(request, "store/home.html", context)


def product_detail(request, slug):
    # try:
    #     product = Product.objects.get(slug=slug, in_stock=True)
    # except Product.DoesNotExist:
    #     raise Http404
    # except Product.MultipleObjectsReturned:
    #     product = Product.objects.filter(slug=slug, in_stock=True).first()

    product = get_object_or_404(Product, slug=slug, in_stock=True)
    context = {
        "product": product,
        "product_qty": range(1, product.qty + 1)
    }
    return render(request, "store/product_detail.html", context)



def search_view(request, *args, **kwargs):
    q = request.GET.get("q")
    qs = None
    if q is not None:
        # lookups = Q(title__icontains=q) | Q(description__icontains=q)
        qs = Product.products.search(q)
    print(qs)

    context = {
        "procucts": qs,
        "search_word": q,
    }
    return render(request, "store/search.html", context)