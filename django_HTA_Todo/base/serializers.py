from rest_framework import serializers
from .models import Task

class TODOSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'id',
            'user',
            'title',
            'description',
            'complete',
            'created'
            
        )
        read_only_fields = (
            'complete',
            'created'
            
        )