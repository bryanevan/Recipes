from django.db import models
from django.db.models import Count
from recipeingredients.models import RecipeIngredient
from ingredients.models import Ingredient
from django.shortcuts import reverse


class Recipe(models.Model):
    class Meta:
        ordering = ["title"]

    title = models.CharField(max_length=50)
    cooking_time = models.PositiveIntegerField(help_text="In minutes")
    description = models.TextField()
    difficulty = models.CharField(max_length=20, default="TBD")
    ingredients = models.ManyToManyField(
        "ingredients.Ingredient", through="recipeingredients.RecipeIngredient"
    )
    pic = models.ImageField(upload_to="recipes", default="no_picture.jpeg")

    def calculate_difficulty(self):
        from recipeingredients.models import (
            RecipeIngredient,
        )

        num_ingredients = RecipeIngredient.objects.filter(recipe=self).count()

        if self.cooking_time < 10 and num_ingredients < 4:
            return "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            return "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            return "Intermediate"
        else:
            return "Hard"

    def save(self, *args, **kwargs):
        self.difficulty = self.calculate_difficulty()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("recipes:recipes_detail", kwargs={"pk": self.pk})
