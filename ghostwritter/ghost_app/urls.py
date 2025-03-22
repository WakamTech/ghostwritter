from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'), # URL pour la page dashboard
]