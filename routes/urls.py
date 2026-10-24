from django.urls import path
from .views import (
    NodeCreateView,
    EdgeCreateView,
    ShortestRouteView,
    RouteHistoryView,
)

app_name = "routes"


urlpatterns = [
    path("nodes", NodeCreateView.as_view(), name="node-create"),
    path("edges", EdgeCreateView.as_view(), name="edge-create"),
    path("routes/shortest", ShortestRouteView.as_view(), name="route-shortest"),
    path("routes/history", RouteHistoryView.as_view(), name="route-history"),
]