from rest_framework import serializers
from base.models import Task

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "complete", "created","user"]