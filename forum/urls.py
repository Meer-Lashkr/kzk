from django.urls import path
from . import views

urlpatterns = [
    path('', views.question_list, name='question_list'),
    path('ask/', views.question_create, name='question_create'),
    path('<int:pk>/', views.question_detail, name='question_detail'),
    path('<int:pk>/edit/', views.question_edit, name='question_edit'),
    path('<int:pk>/delete/', views.question_delete, name='question_delete'),
    path('answer/<int:pk>/edit/', views.answer_edit, name='answer_edit'),
    path('answer/<int:pk>/delete/', views.answer_delete, name='answer_delete'),
    path('<int:question_pk>/accept/<int:answer_pk>/', views.accept_answer, name='accept_answer'),
]
