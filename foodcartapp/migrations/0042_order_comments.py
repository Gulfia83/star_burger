# Generated by Django 3.2.15 on 2024-10-09 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0041_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comments',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name='Комментарии'),
        ),
    ]