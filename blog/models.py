from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from numpy import average

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Zdjęcie',default='default.jpg', upload_to='profile_pics')
    bio = models.TextField()

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):

        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Meal(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class Product(models.Model):

    choices = (
        ('ml', 'mililitr'),
        ('gr', 'gram'),
        ('szt', 'sztuka')
    )

    name = models.CharField(max_length=50, null=False, blank=False, verbose_name='Nazwa produktu', unique=True)
    spoon_weight = models.PositiveIntegerField(null=True, blank=True)
    unit = models.CharField(max_length=20, verbose_name='Jednostka', choices=choices, null=False, blank=False)

    def __str__(self):
        return self.name
    

class Recipe(models.Model):
    host = models.ForeignKey(User, verbose_name='Użytkownik', on_delete=models.CASCADE, null=True)
    meal = models.ForeignKey(Meal, verbose_name='Posiłek', on_delete=models.CASCADE, max_length=100, null=True)
    title = models.CharField('Nazwa dania', max_length=100, null=False)
    description = models.TextField('Przepis', null=False, blank=False)
    participants = models.ManyToManyField(
        to=User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta():
        ordering = ['-created']

    def __str__(self):
        return self.title
    
class Ingredient(models.Model):

    recipe = models.ForeignKey(to=Recipe, null=False, blank=False, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, null=False, blank=False, on_delete=models.CASCADE, verbose_name='Produkt')
    weight = models.PositiveIntegerField(null=True, blank=True, verbose_name='Waga')

 
    def __str__(self):
        return self.product.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    body = models.TextField(null=False, verbose_name='Komentarz')
    rating = IntegerRangeField(min_value=1, max_value=5 ,null=True, blank=True, verbose_name='Ocena')
    image = models.ImageField(null=True, blank=True, upload_to='recipe_pics', verbose_name='Zdjęcie potrawy')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:50]



