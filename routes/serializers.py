from rest_framework import serializers
from .models import Node, Edge


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
    
    def validate(self, data):
        source = data["source"]
        destination = data["destination"]

        if source == destination:
            raise serializers.ValidationError("Source and destination must be different.")

        forward = Edge.objects.filter(source=source, destination=destination).exists()
        backward = Edge.objects.filter(source=destination, destination=source).exists()
        if forward or backward:
            raise serializers.ValidationError("This edge already exists.")

        return data

class ShortestRouteSerializer(serializers.Serializer):
    source = serializers.SlugRelatedField(slug_field="name", queryset=Node.objects.all())
    destination = serializers.SlugRelatedField(slug_field="name", queryset=Node.objects.all())