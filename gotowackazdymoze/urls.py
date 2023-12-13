"""
URL configuration for gotowackazdymoze project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from blog import views
from schema_graph.views import Schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    path('login', views.loginPage, name='login'),
    path('logout', views.logoutPage, name='logout'),
    path('register/', views.registerPage, name='register'),

    path('profile/<str:username>', views.userProfile, name='profile'),
    path('update-user', views.profileUpdate, name='update-user'),

    path('recipe/<str:pk>', views.recipe, name='recipe'),
    path('create-recipe', views.createRecipe, name='create-recipe'),
    path('update-recipe/<str:pk>', views.updateRecipe, name='update-recipe'),
    path('delete-recipe/<str:pk>', views.deleteRecipe, name='delete-recipe'),
    path('delete-comment/<str:pk>', views.deleteComment, name='delete-comment'),
    path('update-comment/<str:pk>', views.updateComment, name='update-comment'),

    path('conversion-factor', views.conversionFactor, name='conversion-factor'),
    path('own-ingredients', views.ownIngredients, name='own-ingredients'),
    path('shopping-list/<str:pk>', views.shoppingList, name='shopping-list'),

    path('api/', include('blog.api.urls')),

    path('__debug__', include("debug_toolbar.urls")),
    
    path("schema/", Schema.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
