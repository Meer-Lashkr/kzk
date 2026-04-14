from django.urls import path
from . import views

urlpatterns = [
    path('', views.coming_soon, name='validation_coming_soon'),
]
