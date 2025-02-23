from django.shortcuts import render
from rest_framework import viewsets
from .models import JobApplication
from .serializers import JobApplicationSerializer

# Create your views here.
class JobApplicationViewset(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
