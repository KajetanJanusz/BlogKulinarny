# Generated by Django 4.2.6 on 2023-10-31 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_alter_comment_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Converter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=20, verbose_name='Produkt')),
                ('factor', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.TextField(verbose_name='Komentarz'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='recipe_pics', verbose_name='Zdjęcie potrawy'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics', verbose_name='Zdjęcie'),
        ),
    ]