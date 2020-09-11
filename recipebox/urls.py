"""recipebox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from homepage.views import index, recipe_detail, author_detail, add_author, add_recipe, login_view, logout_view, edit_recipe_view, fav_recipes_view, add_favorite_recipe_view


urlpatterns = [
    path('', index, name="homepage"),
    path('favorite/add/<str:user_name>/favorites',
         fav_recipes_view, name="favoriterecipes"),
    path('addfavorite/<int:recipe_id>/',
         add_favorite_recipe_view, name="addfavorite"),
    path('recipe/<int:recipe_id>/edit/', edit_recipe_view),
    path('recipe/<int:recipe_id>/', recipe_detail),
    path('author/<int:author_id>/', author_detail),
    path('addrecipe/', add_recipe, name="addrecipe"),
    path('addauthor/', add_author, name="addauthor"),
    path('login/', login_view, name="login_view"),
    path('logout/', logout_view, name="logout_view"),
    path('admin/', admin.site.urls),
]
