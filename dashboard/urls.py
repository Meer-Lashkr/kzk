from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_index, name='dashboard'),
    path('user/', views.user_dashboard, name='user_dashboard'),
    path('moderator/', views.moderator_dashboard, name='moderator_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
]
