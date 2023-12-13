from django.contrib import admin
from .models import Recipe, Meal, Comment, Profile, Ingredient, Product

admin.site.register(Recipe)
admin.site.register(Meal)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Ingredient)
admin.site.register(Product)

