from django.urls import path
from . import views

urlpatterns = [
    path('', views.contribute_home, name='contribute_home'),
    path('correct-this/', views.correct_this_submit, name='correct_this'),
    path('parallel-text/', views.parallel_text_submit, name='parallel_text'),
    path('is-this-correct/', views.is_this_correct_submit, name='is_this_correct'),
    path('my-submissions/', views.my_submissions, name='my_submissions'),
]
