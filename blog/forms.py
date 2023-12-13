from django import forms
from .models import Recipe, Profile, Comment, Ingredient, Product
from django.contrib.auth.models import User
from django.forms import formset_factory, modelformset_factory


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['host', 'meal', 'title', 'description', 'ingredients']
        exclude = ['host', 'ingredients']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body', 'image', 'rating']
        widgets = {'body': forms.Textarea(attrs={"rows":"2"})}

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['product', 'weight']

IngredientFormset = formset_factory(IngredientForm, extra=1)

OwnIngredientsFormset = formset_factory(IngredientForm, extra=1)

class ConverterForm(forms.ModelForm):

    products = Product.objects.filter(spoon_weight__isnull=False)

    name = forms.ModelChoiceField(queryset=products, label='Nazwa produktu')
    spoons = forms.IntegerField(label='Łyżki', min_value=1)

    class Meta:
        model = Product
        fields = ['name', 'spoons']

class EmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
