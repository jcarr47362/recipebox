from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from homepage.models import Recipe, Author
from homepage.forms import AddRecipeForm, AddAuthorForm, LoginForm


# Create your views here.


def index(request):
    my_recipes = Recipe.objects.all()
    return render(request, "index.html", {"recipes": my_recipes, "welcome_name": "Rockstars"})


def recipe_detail(request, recipe_id):
    my_recipe = Recipe.objects.filter(id=recipe_id).first()
    return render(request, "recipe_detail.html", {"recipe": my_recipe})


def author_detail(request, author_id):
    # my_recipe = Recipe.objects.filter(author=author_id)
    # my_author = Author.objects.filter(id=author_id).first()
    my_recipe = Author.objects.filter(id=author_id).first()
    return render(request, "author_detail.html", {"author": my_recipe})


@login_required
def add_author(request):
    if request.method == "POST":
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = User.objects.create_user(username=data.get("username"), password=data.get("password"))
            Author.objects.create(
                name = data.get("name"),
                bio = data.get("bio"),
                user = new_user
            )
            return HttpResponseRedirect(request.GET.get("next", reverse("homepage")))

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
                time_required = data.get('time_required'),
                instructions = data.get('instructions')

            )
            return HttpResponseRedirect(reverse("homepage"))

    form = AddRecipeForm()
    return render(request, "generic_form.html", {'form': form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get("username"), password=data.get("password"))
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
