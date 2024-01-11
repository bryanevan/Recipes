from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Ingredient


class IngredientModelTest(TestCase):
    # test for ingredient name
    def test_create_ingredient(self):
        ingredient = Ingredient.objects.create(name="Salt")
        self.assertEqual(ingredient.name, "Salt")

    # test for long ingredient name
    def test_create_ingredient_long_name(self):
        ingredient = Ingredient.objects.create(name="a" * 256)
        self.assertRaises(ValidationError)

    # test for ingredient string representation
    def test_ingredient_string_representation(self):
        ingredient = Ingredient.objects.create(name="Pepper")
        self.assertEqual(str(ingredient), "Pepper")