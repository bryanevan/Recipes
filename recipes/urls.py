from django.urls import path
from .views import (
    recipes_home,
    RecipesDetailView,
    RecipesListView,
    export_recipes_csv,
    export_single_recipe_csv,
    generate_chart,
    about_view,
    create_view,
)

app_name = "recipes"

urlpatterns = [
    path("", recipes_home, name="recipes_home"),
    path("recipes/", RecipesListView.as_view(), name="recipes_list"),
    path("recipes/<pk>", RecipesDetailView.as_view(), name="recipes_detail"),
    path("recipes/export/", export_recipes_csv, name="export_csv"),
    path("generate-chart/", generate_chart, name="generate_chart"),
    path(
        "export_single_recipe/<int:recipe_id>/",
        export_single_recipe_csv,
        name="export_single_recipe_csv",
    ),
    path("about/", about_view, name="about"),
    path("create/", create_view, name="create"),
]
