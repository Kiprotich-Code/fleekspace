from django.urls import path, include
from rest_framework import routers
from .views import JobApplicationViewset

# urls 
router = routers.DefaultRouter()
router.register(r'applications', JobApplicationViewset)

urlpatterns = [
    path('v1/', include(router.urls)),
]