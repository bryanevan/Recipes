"""
URL configuration for recipe_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    login_view,
    logout_view,
    recipes_home,
    about_view,
    list_view,
    create_view,
)
from django.views.generic import TemplateView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("recipes.urls")),
    path("home/", recipes_home, name="recipes_home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path(
        "success/",
        TemplateView.as_view(template_name="recipes/success.html"),
        name="success",
    ),
    path("__reload__/", include("django_browser_reload.urls", namespace="reload")),
    path("about/", about_view, name="about"),
    path("create/", create_view, name="create"),
]

urlpatterns = (
    urlpatterns
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
