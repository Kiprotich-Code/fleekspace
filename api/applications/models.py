from django.db import models

# Create your models here.
class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('interview', 'Interview'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    ]

    PRIORITY = [
        ('High', 'high'),
        ('Medium', 'medium'),
        ('Low', 'low'),
    ]

    job_title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    stage = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=10, choices=PRIORITY, default='medium')
    application_status = models.BooleanField(default=False)
    applied_on = models.DateField()
    deadline = models.DateField()
    link = models.TextField(null=True, blank=True)  # Optional, for interview results
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.job_title} at {self.company}"