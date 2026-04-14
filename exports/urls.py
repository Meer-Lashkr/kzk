from django.urls import path
from . import views

urlpatterns = [
    path('corrections/csv/', views.export_corrections_csv, name='export_corrections_csv'),
    path('corrections/json/', views.export_corrections_json, name='export_corrections_json'),
    path('parallel/csv/', views.export_parallel_csv, name='export_parallel_csv'),
    path('parallel/json/', views.export_parallel_json, name='export_parallel_json'),
    path('judgments/csv/', views.export_judgments_csv, name='export_judgments_csv'),
    path('judgments/json/', views.export_judgments_json, name='export_judgments_json'),
]
