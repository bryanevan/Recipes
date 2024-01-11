from django.test import TestCase
from ingredients.models import Ingredient
from recipeingredients.models import RecipeIngredient
from recipes.models import Recipe
from django.shortcuts import reverse
from django.contrib.auth.models import User
from recipes.forms import RecipeSearchForm

# Create your tests here.


class RecipeModelTest(TestCase):
    def setUp(self):
        # Create a test user and log them in for the views requiring login
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

    def test_recipe_string_representation(self):
        recipe = Recipe.objects.create(
            id=1, title="Test Recipe", cooking_time=30, description="Test description"
        )
        self.assertEqual(str(recipe), "Test Recipe")

    # test for recipe difficulty (easy)
    def test_recipe_easy_difficulty(self):
        recipe = Recipe.objects.create(
            id=1, title="Test Recipe", cooking_time=5, description="Test description"
        )
        ingredient1 = Ingredient.objects.create(name="Ingredient 1")
        ingredient2 = Ingredient.objects.create(name="Ingredient 2")
        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient1)
        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient2)

        # force the recipe to update its difficulty level after ingredients are added
        recipe.save()

        self.assertEqual(recipe.difficulty, "Easy")

    # test for recipe difficulty (medium)
    def test_recipe_medium_difficulty(self):
        ingredient1 = Ingredient.objects.create(name="Ingredient 1")
        ingredient2 = Ingredient.objects.create(name="Ingredient 2")
        ingredient3 = Ingredient.objects.create(name="Ingredient 3")
        ingredient4 = Ingredient.objects.create(name="Ingredient 4")
        ingredient5 = Ingredient.objects.create(name="Ingredient 5")

        recipe = Recipe.objects.create(
            id=1, title="Test Recipe", cooking_time=5, description="Test description"
        )

        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient1)
        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient2)
        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient3)
        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient4)
        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient5)

        # force the recipe to update its difficulty level after ingredients are added
        recipe.save()

        self.assertEqual(recipe.difficulty, "Medium")

    # test for recipe difficulty (intermediate)
    def test_recipe_intermediate_difficulty(self):
        ingredient1 = Ingredient.objects.create(name="Ingredient 1")
        ingredient2 = Ingredient.objects.create(name="Ingredient 2")
        ingredient3 = Ingredient.objects.create(name="Ingredient 3")

        recipe = Recipe.objects.create(
            id=1, title="Test Recipe", cooking_time=15, description="Test description"
        )

        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient1)
        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient2)
        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient3)

        # force the recipe to update its difficulty level after ingredients are added
        recipe.save()

        self.assertEqual(recipe.difficulty, "Intermediate")

    # test for recipe difficulty (hard)
    def test_recipe_hard_difficulty(self):
        ingredient1 = Ingredient.objects.create(name="Ingredient 1")
        ingredient2 = Ingredient.objects.create(name="Ingredient 2")
        ingredient3 = Ingredient.objects.create(name="Ingredient 3")
        ingredient4 = Ingredient.objects.create(name="Ingredient 4")
        ingredient5 = Ingredient.objects.create(name="Ingredient 5")

        recipe = Recipe.objects.create(
            id=1, title="Test Recipe", cooking_time=30, description="Test description"
        )

        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient1)
        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient2)
        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient3)
        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient4)
        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient5)

        # force the recipe to update its difficulty level after ingredients are added
        recipe.save()

        self.assertEqual(recipe.difficulty, "Hard")

    # test the recipe ingredients relationship
    def test_recipe_ingredients(self):
        recipe = Recipe.objects.create(
            id=1, title="Test Recipe", cooking_time=30, description="Test description"
        )
        ingredient1 = Ingredient.objects.create(name="Ingredient 1")
        ingredient2 = Ingredient.objects.create(name="Ingredient 2")
        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient1)
        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient2)
        self.assertEqual(recipe.ingredients.count(), 2)

    # test get_absolute_url
    def test_get_absolute_url(self):
        recipe = Recipe.objects.create(
            id=1, title="Test Recipe", cooking_time=30, description="Test description"
        )
        self.assertEqual(recipe.get_absolute_url(), "/recipes/1")

    # test RecipesListView
    def test_recipes_list_view(self):
        response = self.client.get("/recipes/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipes_list.html")

    # test context data in RecipesListView
    def test_recipes_list_view_context_data(self):
        recipe = Recipe.objects.create(
            id=1, title="Test Recipe", cooking_time=30, description="Test description"
        )
        response = self.client.get("/recipes/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["recipes"]), 1)
        self.assertEqual(response.context["recipes"][0], recipe)

    # test RecipesDetailView
    def test_recipes_detail_view(self):
        recipe = Recipe.objects.create(
            id=1, title="Test Recipe", cooking_time=30, description="Test description"
        )
        response = self.client.get("/recipes/1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipes_detail.html")

    # test context data in RecipesDetailView
    def test_recipes_detail_view_context_data(self):
        recipe = Recipe.objects.create(
            id=1, title="Test Recipe", cooking_time=30, description="Test description"
        )
        response = self.client.get("/recipes/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["recipe"], recipe)

    # test recipes_home_view
    def test_recipes_home_view(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipes_home.html")


class RecipeSearchFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create some test data for the Recipe and Ingredient models
        ingredient1 = Ingredient.objects.create(name="Ingredient 1")
        ingredient2 = Ingredient.objects.create(name="Ingredient 2")
        recipe1 = Recipe.objects.create(id=1, title="Recipe 1", cooking_time=30)
        recipe2 = Recipe.objects.create(id=2, title="Recipe 2", cooking_time=60)
        recipe1.ingredients.add(ingredient1)
        recipe2.ingredients.add(ingredient2)

        # Create additional recipes
        for i in range(3, 13):  # Creates 10 additional recipes with ids 3 to 12
            recipe = Recipe.objects.create(
                id=i, title=f"Recipe {i}", cooking_time=(i + 1) * 10
            )
            recipe.ingredients.add(ingredient1)
            recipe.ingredients.add(ingredient2)

    def setUp(self):
        # Create a test user and log them in for the views requiring login
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

    def test_form_fields(self):
        form_data = {
            "Recipe_Name": "Recipe 1",
            "Ingredients": [1],
            "chart_type": "#1",
        }
        form = RecipeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_missing_data(self):
        form_data = {}  # No data provided
        form = RecipeSearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["__all__"][0],
            "Please enter a recipe name or select an ingredient.",
        )

    def test_recipe_list_view(self):
        response = self.client.get("/recipes/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipes_list.html")

    def test_pagination(self):
        response = self.client.get("/recipes/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue("recipes" in response.context)
        self.assertTrue(response.context["is_paginated"])

    def test_chart_generation(self):
        form_data = {
            "Recipe_Name": "",
            "Ingredients": [1],
            "chart_type": "#1",
        }
        response = self.client.get("/recipes/", form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("chart_image" in response.context)

    def test_view_protected(self):
        self.client.logout()
        response = self.client.get("/recipes/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/?next=/recipes/")

    def test_export_recipes_csv_view(self):
        response = self.client.get("/recipes/export/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")

    def test_generate_chart_view(self):
        form_data = {
            "Recipe_Name": "",
            "Ingredients": [1],
            "chart_type": "#1",
        }
        response = self.client.get("/generate-chart/", form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("chart_image" in response.json())
