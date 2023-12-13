from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Recipe, Meal, Comment, Ingredient, Product
from .forms import RecipeForm, UserUpdateForm, ProfileUpdateForm, CommentForm, IngredientFormset, OwnIngredientsFormset, ConverterForm, EmailForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

def registerPage(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Coś poszło nie tak :/')

    return render(request, 'login_register.html', {'form': form})


def loginPage(request):
    page = 'login'
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Użytkownik nie istnieje')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Zalogowano poprawnie.')
            return redirect('home')

    context = {'page': page}
    return render(request, 'login_register.html', context)


@login_required
def logoutPage(request):
    logout(request)
    return redirect('home')


def userProfile(request, username):
    user = User.objects.get(username=username)
    recipes = Recipe.objects.filter(host=user)
    comments = Comment.objects.filter(user_id=user.id).order_by('-created')
    context = {'comments': comments, 'user': user, 'recipes': recipes}
    return render(request, 'profile.html', context=context)


@login_required
def profileUpdate(request):
    form_u = UserUpdateForm(instance=request.user)
    form_p = ProfileUpdateForm(instance=request.user.profile)
    if request.method == "POST":
        form_u = UserUpdateForm(request.POST, 
                                instance=request.user)
        form_p = ProfileUpdateForm(request.POST,
                                   request.FILES, 
                                   instance=request.user.profile)
        if form_u.is_valid() and form_p.is_valid():
            form_u.save()
            form_p.save()
            messages.success(request, 'Konto zaktualizowane!')
            return redirect('profile', username=request.user.username)
        
        else:
            form_u = UserUpdateForm(instance=request.user)
            form_p = ProfileUpdateForm(instance=request.user.profile)

        
    context = {
        'form_u': form_u,
        'form_p': form_p
    }
            
    return render(request, 'update_user.html', context=context)


def home(request):
    q = request.GET.get('search')
    if q != None:
        recipes = Recipe.objects.filter(
            Q(meal__name__icontains=q) |
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(host__username__icontains=q)
            )
    else:
        recipes = Recipe.objects.all()
    count = recipes.count()
    meals = Meal.objects.all()
    comments = Comment.objects.all().order_by('-created')
    ingredients = Ingredient.objects.all()
    
    paginator = Paginator(recipes, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    
    context = {'recipes' : recipes,
                'meals': meals,
                'count' : count,
                'comments': comments,
                'ingredients': ingredients,
                'page_obj': page_obj
                }
    
    return render(request, 'home.html', context=context)


def recipe(request, pk):
    recipes_all = Recipe.objects.all()
    recipe = Recipe.objects.get(id=pk)
    ingredients = Ingredient.objects.filter(recipe_id=pk)
    comments = recipe.comment_set.all().order_by('-created')
    participants = recipe.participants.all()
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.recipe = recipe
            comment.save()
            recipe.participants.add(request.user)

        return redirect('recipe', pk=recipe.id)

    context = {'recipe': recipe,
               'recipes_all': recipes_all,
               'comments': comments, 
               'participants': participants,
               'form': form,
               'ingredients': ingredients}
    
    return render(request, 'recipe.html', context=context)


@login_required
def createRecipe(request):
    form_r = RecipeForm()
    formset_i = IngredientFormset()
    if request.method == "POST":
        form_r = RecipeForm(request.POST)
        formset_i = IngredientFormset(request.POST)
        if form_r.is_valid() and formset_i.is_valid():
            recipe = form_r.save(commit=False)
            recipe.host = request.user
            recipe.save()
            for form in formset_i:
                ingredient_weight = form.cleaned_data.get('weight')
                ingredient_product = form.cleaned_data.get('product')
                if ingredient_weight:
                    Ingredient(recipe_id=recipe.id,product=ingredient_product, weight=ingredient_weight).save()
            return redirect('home')
    
    context = {'form_r' : form_r, 'formset_i': formset_i}
    return render(request, 'create_recipe.html', context)


@login_required
def updateRecipe(request, pk):
    fields = Recipe.objects.get(id=pk)
    form = RecipeForm(instance=fields)
    if request.method == "POST":
        form = RecipeForm(request.POST, instance=fields)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form' : form}
    return render(request, 'update_recipe.html', context)


@login_required
def deleteRecipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    if request.method == "POST":
        recipe.delete()
        return redirect('home')

    return render(request, 'delete_recipe.html', {'recipe': recipe})


@login_required
def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)
    recipe = Recipe.objects.get(comment=pk)

    if request.method == "POST":
        comment.delete()
        comment_user = Comment.objects.filter(recipe_id=recipe.id, user_id=request.user.id).count()
        if comment_user == 0:
            recipe.participants.remove(request.user)
        return redirect('recipe', pk=comment.recipe.id)

    return render(request, 'delete_comment.html', {'comment': comment})

@login_required
def updateComment(request, pk):
    comment = Comment.objects.get(id=pk)
    form = CommentForm(instance=comment)

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            form.save()
        return redirect('recipe', pk=comment.recipe.id)

    context = {'form': form}

    return render(request, 'update-comment.html', context=context)


def conversionFactor(request):
    form = ConverterForm()
    product_data = list(Product.objects.values())
    if request.method == 'POST':
        product = Product.objects.get(id=request.POST['name'])
        output = int(request.POST['spoons']) * int(product.spoon_weight)

        context = {'output': output,
                    'product': product}
        
        return render(request, 'conversion_result.html', context=context)

    context = {'form': form}
    return render(request, 'conversion_factor.html', context=context)

def ownIngredients(request):
    formset = OwnIngredientsFormset()
    if request.method == 'POST':
        formset = OwnIngredientsFormset(request.POST)
        products_list = []
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data != {}:
                    products_list.append(form.cleaned_data['product'].name)

        recipes = Recipe.objects.all()
        recipes_output = []
        for recipe in recipes:
            ingredients = Ingredient.objects.filter(recipe_id=recipe.id)
            ingredients_list = [ingredient.product.name for ingredient in ingredients]
            p_list = products_list.copy()
            for product in p_list:
                if product in ingredients_list:
                    ingredients_list.remove(product)
                    if len(ingredients_list) == 0:
                        recipes_output.append(recipe)

        context = {'recipes_output': recipes_output}
        return render(request, 'own-ingredients-result.html', context=context)
    
    context = {'formset':formset}
    return render(request, 'own-ingredients.html', context=context)


def shoppingList(request, pk):
    form = EmailForm()
    recipe = Recipe.objects.get(id=pk)
    ingredients = Ingredient.objects.filter(recipe_id=pk)
    if request.method =='POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            send_mail(
                subject=f'Lista zakupów do przepisu: {recipe.title}',
                message=f'Produkty: {[ingredient.product for ingredient in ingredients]}',
                from_email='settings.EMAIL_HOST_USER',
                recipient_list=['email'],
                fail_silently=False
            )
            messages.success(request, 'Lista została wysłana')
        else:
            messages.error(request, 'Wiadomość nie została wysłana, skontaktuj się z administratorem')
            
            return redirect('recipe', id=pk)
    
    context = {
        'form': form
    }
    
    return render(request, 'send-shopping-list.html', context=context)



