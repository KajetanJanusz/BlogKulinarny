# Generated by Django 3.2.23 on 2023-11-09 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0026_auto_20231107_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='unit',
            field=models.CharField(choices=[('ml', 'mililitr'), ('gr', 'gram'), ('szt', 'sztuka')], max_length=20, verbose_name='Jednostka'),
        ),
    ]