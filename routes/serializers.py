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