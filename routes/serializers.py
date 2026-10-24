from rest_framework import serializers
from .models import Node, Edge, RouteQuery


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = '__all__'

class EdgeSerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(slug_field='name', queryset=Node.objects.all())
    destination = serializers.SlugRelatedField(slug_field="name", queryset=Node.objects.all())
    class Meta:
        model = Edge
        fields = ["id", "source", "destination", "latency"]
        
    def validate_latency(self, value):
        if value <= 0:
            raise serializers.ValidationError("Latency must be greater than 0.")
        return value