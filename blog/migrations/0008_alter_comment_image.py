# Generated by Django 4.2.6 on 2023-10-31 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_comment_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='recipe_pics'),
        ),
    ]
