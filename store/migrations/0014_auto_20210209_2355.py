# Generated by Django 3.1.4 on 2021-02-09 17:55

from django.db import migrations, models
import store.validators


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_userbookrelation_discount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userbookrelation',
            name='discount',
        ),
        migrations.AddField(
            model_name='book',
            name='discount',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[store.validators.validate_percent_field]),
        ),
    ]