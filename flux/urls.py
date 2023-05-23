from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import flux, posts

urlpatterns = [
    path("flux/", flux, name="flux"),
    path("posts/", posts, name="posts"),
]
