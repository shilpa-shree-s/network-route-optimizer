# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Edge, Node, RouteQuery

from .serializers import NodeSerializer, EdgeSerializer, ShortestRouteSerializer
from .route_finder import find_shortest_route

def build_graph():
    # every server is a key, even ones with no connections
    graph = {node.name: {} for node in Node.objects.all()}

    for edge in Edge.objects.select_related("source", "destination"):
        # connections are two-way, so adding both directions
        graph[edge.source.name][edge.destination.name] = edge.latency
        graph[edge.destination.name][edge.source.name] = edge.latency

    return graph

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

class ShortestRouteView(APIView):
    def post(self, request):
        serializer = ShortestRouteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        source = serializer.validated_data["source"].name
        destination = serializer.validated_data["destination"].name

        graph = build_graph()
        result = find_shortest_route(graph, source, destination)

        if result is None:
            return Response(
                {"error": f"No path exists between {source} and {destination}"},
                status=status.HTTP_404_NOT_FOUND,
            )

        total_latency, path = result

        RouteQuery.objects.create(
            source=source,
            destination=destination,
            total_latency=total_latency,
            path=path,
        )

        return Response(
            {"total_latency": total_latency, "path": path},
            status=status.HTTP_200_OK,
        )