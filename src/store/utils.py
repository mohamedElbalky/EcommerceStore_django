from random import randint

from django.utils.text import slugify


def get_unique_slug(instance, instance_field_to_slugify, instance_slug):
    klass = instance.__class__
    if instance_slug is not None:
        slug_ = slugify(instance_field_to_slugify)
        qs = klass.objects.filter(slug=slug_).exclude(id=instance.id)
        if qs.exists():
            slug_ = instance_slug
        else:
            qs = slug_
    else:
        slug_ = slugify(instance_field_to_slugify)

    qs = klass.objects.filter(slug=slug_).exclude(id=instance.id)
    if qs.exists():
        rand_int = randint(300_000, 600_000)
        slug_ = f"{slug_}{rand_int}"
        return get_unique_slug(instance, instance_field_to_slugify, instance_slug=slug_)
    return slug_



