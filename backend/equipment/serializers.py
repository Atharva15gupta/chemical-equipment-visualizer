from rest_framework import serializers
from .models import Dataset


class DatasetSerializer(serializers.ModelSerializer):
    """Serializer for Dataset model"""
    
    class Meta:
        model = Dataset
        fields = [
            'id', 
            'filename', 
            'uploaded_at', 
            'total_count',
            'avg_flowrate',
            'avg_pressure',
            'avg_temperature',
            'type_distribution'
        ]
        read_only_fields = ['id', 'uploaded_at']


class UploadResponseSerializer(serializers.Serializer):
    """Serializer for upload response"""
    message = serializers.CharField()
    dataset_id = serializers.IntegerField()
    summary = serializers.DictField()
    data = serializers.ListField()
