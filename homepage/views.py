from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from homepage.models import Recipe, Author
from homepage.forms import AddRecipeForm, AddAuthorForm, LoginForm


# Create your views here.


def index(request):
    my_recipes = Recipe.objects.all()
    return render(request, "index.html", {"recipes": my_recipes, "welcome_name": "Rockstars"})


def fav_recipes_view(request, user_name):
    requesting_user = request.user
    fav_recipes = Recipe.objects.filter(username=user_name).first()
    requesting_user.favorite_recipes.add()
    return render(request, "favorite_recipes.html", {"fav_recipes": fav_recipes})


def add_favorite_recipe_view(request, recipe_id):
    fav_recipe = Recipe.objects.get(id=recipe_id)
    logged_in_user = Author.objects.get(user=request.user)
    logged_in_user.favorite_recipes.add(fav_recipe)
    logged_in_user.save()
    print(logged_in_user.favorite_recipes.all())
    return HttpResponseRedirect(reverse("homepage"))


def recipe_detail(request, recipe_id):
    my_recipe = Recipe.objects.filter(id=recipe_id).first()
    return render(request, "recipe_detail.html", {"recipe": my_recipe})


def author_detail(request, author_id):
    # my_author = Author.objects.filter(id=author_id).first()
    my_author = Author.objects.filter(id=author_id).first()
    my_recipes = Recipe.objects.filter(author=my_author)
    return render(request, "author_detail.html", {"author": my_author, "recipes": my_recipes})


@login_required
def add_author(request):
    if request.user.is_staff:
        if request.method == "POST":
            form = AddAuthorForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                print("NAME", data.get("name"))
                print("BIO", data.get("bio"))
                print("PASSWORD", data.get("password"))
                new_user = User.objects.create_user(
                    username=data.get("name"),
                    password=data.get("password")
                )
                Author.objects.create(
                    name=data.get("name"),
                    bio=data.get("bio"),
                    user=new_user
                )
                return HttpResponseRedirect(reverse("homepage"))
    else:
        messages.info(request, "You are not a staff member")
        return redirect("homepage")

    form = AddAuthorForm()
    return render(request, "generic_form.html", {"form": form})


@login_required
def add_recipe(request):
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data.get('title'),
                description=data.get('description'),
                author=request.user.author,
                time_required=data.get('time_required'),
                instructions=data.get('instructions')

            )
            return HttpResponseRedirect(reverse("homepage"))

    form = AddRecipeForm()
    return render(request, "generic_form.html", {'form': form})


@login_required
def edit_recipe_view(request, recipe_id):
    edit_recipe = Recipe.objects.get(id=recipe_id)
    if request.method == "POST":
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            edit_recipe.title = data['title']
            edit_recipe.description = data['description']
            edit_recipe.time_required = data['time_required']
            edit_recipe.instructions = data['instructions']
            edit_recipe.save()
        return HttpResponseRedirect(reverse("homepage"))

    data = {
        "title": edit_recipe.title,
        "description": edit_recipe.description,
        "time_required": edit_recipe.time_required,
        "instructions": edit_recipe.instructions
    }
    form = AddRecipeForm(initial=data)
    return render(request, "generic_form.html", {'form': form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get(
                "username"), password=data.get("password"))
            if user:
                login(request, user)
            # return HttpResponseRedirect(reverse("homepage"))
                return HttpResponseRedirect(request.GET.get("next", reverse("homepage")))
    form = LoginForm()
    return render(request, "generic_form.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))


"""
    localhost:8000/
    localhost:8000/recipe/3
    """
