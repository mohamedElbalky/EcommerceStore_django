# Generated by Django 4.0.6 on 2022-09-12 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='braintree_id',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
