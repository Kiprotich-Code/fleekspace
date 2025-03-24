from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("users/", include("users.urls", namespace="users")),
    path("blog/", include("blog.urls", namespace="blog")),
    path("api/", include("applications.urls")),
]
