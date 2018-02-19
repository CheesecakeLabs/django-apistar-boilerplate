from apistar import Include
from django.contrib import admin
from django.urls import path

from authentication.routes import routes as auth_routes


urlpatterns = [
    path('admin/', admin.site.urls),
]
