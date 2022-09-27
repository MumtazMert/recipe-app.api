# URL mappings for the recipe app

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from recipe import views

# We create a default router
# Registering a viewset to that router
# Recipe viewset will have auto generated URLs
router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)
router.register('tags', views.TagViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]
