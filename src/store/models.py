

from email.policy import default
from itertools import product
from random import randint

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q

USER = settings.AUTH_USER_MODEL





class Category(models.Model):
    name = models.CharField(max_length=225, db_index=True)
    slug = models.SlugField(max_length=225, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "categories"

    def get_products_by_category(self):
        products = self.product_catogery.all()
        return products

    def get_absolute_url(self, *args, **kwargs):
        return reverse("shope:all_products_by_category", args=[self.slug])

    def __str__(self):
        return str(self.name)


# def create_folder_for_image(instance):
#     path = f"images/{instance.title}"
#     return path


class ProductModelMAnager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(in_stock=True, is_active=True)

    def search(self, query):
        lookups = Q(title__icontains=query) | Q(description__icontains=query)
        return self.get_queryset().filter(lookups)

class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name="product_catogery", on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        USER, related_name="product_creator", on_delete=models.CASCADE)
    title = models.CharField(max_length=225)
    # author of the book
    author = models.CharField(max_length=225, default="admin")
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to="images/", default="images/no_photo.jpg")
    slug = models.SlugField(max_length=225, blank=True, null=True, unique=True)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    products = ProductModelMAnager()

    class Meta:
        verbose_name_plural = "products"
        ordering = ("-updated", "-created")

    # def save(self, *args, **kwargs):
    #     if self.slug is None:
    #         self.slug = slugify(self.title)
    #     super(Product, self).save(*args, **kwargs) # Call the real save() method

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("store:product_detail", kwargs={"slug": self.slug})


# def creat_image_folder_pre_save(sender, instance, *args, **kwargs):
#     slug = instance.slug
#     instance.image.upload_to = f"images/{slug}"


# pre_save.connect(creat_image_folder_pre_save, sender=Product)
