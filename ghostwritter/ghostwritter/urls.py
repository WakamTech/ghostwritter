from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ghost_app.urls')), # Inclure les URLs de ghost_app
]