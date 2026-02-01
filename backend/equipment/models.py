from django.db import models
from django.contrib.auth.models import User
import json


class Dataset(models.Model):
    """Model to store uploaded datasets and their summaries"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='datasets')
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Summary statistics stored as JSON
    total_count = models.IntegerField(default=0)
    avg_flowrate = models.FloatField(default=0.0)
    avg_pressure = models.FloatField(default=0.0)
    avg_temperature = models.FloatField(default=0.0)
    type_distribution = models.JSONField(default=dict)
    
    # Store the CSV file path
    csv_file = models.FileField(upload_to='uploads/', null=True, blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        
    def __str__(self):
        return f"{self.filename} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"
    
    @classmethod
    def cleanup_old_datasets(cls, user, keep_count=5):
        """Keep only the last N datasets for a user"""
        old_datasets = cls.objects.filter(user=user)[keep_count:]
        for dataset in old_datasets:
            if dataset.csv_file:
                dataset.csv_file.delete()
            dataset.delete()
