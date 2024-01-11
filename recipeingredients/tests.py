from django.test import TestCase
from recipes.models import Recipe
from ingredients.models import Ingredient
from recipeingredients.models import RecipeIngredient

# Create your tests here.


class RecipeIngredientModelTest(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(title="Test Recipe", cooking_time=30)
        self.ingredient = Ingredient.objects.create(name="Test Ingredient")
        self.recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe, ingredient=self.ingredient
        )

    def test_recipe_ingredient_relationship(self):
        self.assertEqual(self.recipe_ingredient.recipe, self.recipe)
        self.assertEqual(self.recipe_ingredient.ingredient, self.ingredient)

    def test_recipe_ingredient_string_representation(self):
        expected_string = f"{self.ingredient} - {self.recipe}"
        self.assertEqual(str(self.recipe_ingredient), expected_string)

    def test_recipe_ingredient_attributes(self):
        self.assertEqual(self.recipe_ingredient.recipe.title, "Test Recipe")
        self.assertEqual(self.recipe_ingredient.ingredient.name, "Test Ingredient")