from .models import Category


def categories(request):
    categories = Category.objects.all()
    # you will target categories in html page py using "categories"
    context = {
        "categories": categories
    }
    return context


