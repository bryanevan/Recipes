from django import forms
from .models import Ingredient
from recipeingredients.models import RecipeIngredient
from ingredients.models import Ingredient


CHART_CHOICES = (
    ("#1", "Bar Chart"),
    ("#2", "Pie Chart"),
    ("#3", "Line Chart"),
)


class RecipeSearchForm(forms.Form):
    Recipe_Name = forms.CharField(
        required=False,
        max_length=50,
        label="Recipe Name",
        widget=forms.TextInput(
            attrs={
                "class": "text-black" "form-item",
                "placeholder": "Enter Recipe Name",
            }
        ),
    )
    Ingredients = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Ingredient.objects.all(),
        label="Ingredient(s)",
        widget=forms.SelectMultiple(attrs={"class": "form-item"}),
    )
    chart_type = forms.ChoiceField(
        choices=CHART_CHOICES, widget=forms.Select(attrs={"class": "form-item"})
    )

    def clean(self):
        cleaned_data = super().clean()
        recipe_name = cleaned_data.get("Recipe_Name")
        ingredients = cleaned_data.get("Ingredients")

        if not recipe_name and not ingredients:
            raise forms.ValidationError(
                "Please enter a recipe name or select an ingredient."
            )
        return cleaned_data


class CreateRecipeForm(forms.Form):
    title = forms.CharField(
        max_length=50, required=True, error_messages={"required": ""}
    )
    cooking_time = forms.IntegerField(
        help_text="In minutes", required=True, error_messages={"required": ""}
    )
    description = forms.CharField(
        widget=forms.Textarea, required=True, error_messages={"required": ""}
    )
    ingredients = forms.CharField(
        widget=forms.Textarea,
        required=True,
        help_text="Enter each ingredient separated by a comma or a newline.",
        error_messages={"required": ""},
    )
    pic = forms.ImageField(required=False)
