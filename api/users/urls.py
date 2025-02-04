from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = "users"

# urlpatterns 
urlpatterns = [
    path("register/", views.UserRegisterAPIView.as_view(), name="create-user"),
    path("login/", views.UserLoginAPIView.as_view(), name="login-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("logout/", views.UserLogoutAPIView.as_view(), name="logout-user"),
    path("", views.UserAPIView.as_view(), name="user-info"),
    path("profile/", views.UserProfileAPIView.as_view(), name="user-profile"),
    path("profile/avatar/", views.UserAvatarAPIView.as_view(), name="user-avatar"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
