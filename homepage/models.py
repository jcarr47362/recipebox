from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=80)
    bio = models.TextField(max_length=80)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    favorite_recipes = models.ManyToManyField("Recipe", blank=True, related_name="favorite_recipes")

    def __str__(self):
        return self.name


class Profile(models.Model):
    pass


class Recipe(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    time_required = models.CharField(max_length=50)
    instructions = models.TextField()

    def __str__(self):
        return f"{self.title} - {self.author.name}"
