# Generated by Django 3.1.4 on 2021-02-01 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_book_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='owner',
        ),
    ]
