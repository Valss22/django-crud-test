# Generated by Django 3.1.4 on 2021-02-10 06:21

from django.db import migrations, models
import store.validators


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_auto_20210210_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbookrelation',
            name='discount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, validators=[store.validators.validate_percent_field]),
        ),
    ]
