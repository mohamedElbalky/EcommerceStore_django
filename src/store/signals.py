"""signals for saving models"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Category, Product
from .utils import get_unique_slug


@receiver(pre_save, sender=Category)
def create_slug_category_pre_save(sender, instance, *args, **kwargs):
    """pre_save functionality for Category model"""
    instance.slug = get_unique_slug(instance, instance.name, instance.slug)



@receiver(post_save, sender=Category)
def create_slug_category_post_save(sender, instance, created, *args, **kwargs):
    """post_save functionality for Category model"""
    if instance.slug is None:
        instance.slug = get_unique_slug(instance, instance.name)
        instance.save()



@receiver(pre_save, sender=Product)
def create_slug_product_pre_save(sender, instance, *args, **kwargs):
    """pre_save functionality for Product model"""
    instance.slug = get_unique_slug(instance, instance.title, instance.slug)


@receiver(post_save, sender=Product)
def create_slug_product_post_save(sender, instance, created, *args, **kwargs):
    """post_save functionality for Product model"""
    if created:
        instance.slug = get_unique_slug(instance, instance.title, instance.slug)
        instance.save()

# post_save.connect(create_slug_product_post_save, Product)
