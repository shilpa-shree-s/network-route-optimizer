# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Edge, Node

from .serializers import NodeSerializer, EdgeSerializer

class NodeCreateView(APIView):
    def post(self, request):
        serializer = NodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EdgeCreateView(APIView):
    def post(self, request):
        serializer = EdgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def build_graph():
    # every server is a key, even ones with no connections
    graph = {node.name: {} for node in Node.objects.all()}

    for edge in Edge.objects.select_related("source", "destination"):
        # connections are two-way, so adding both directions
        graph[edge.source.name][edge.destination.name] = edge.latency
        graph[edge.destination.name][edge.source.name] = edge.latency

    return graph