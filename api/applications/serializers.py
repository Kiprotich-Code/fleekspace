from rest_framework import serializers
from .models import JobApplication


# serializers 
class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['job_title', 'company', 'description', 'stage', 'priority',  'applied_on', 'application_status', 'applied_on', 'deadline', 'link', 'note' ]