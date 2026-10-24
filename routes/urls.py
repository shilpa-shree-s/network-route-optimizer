from django.urls import path
from .views import NodeCreateView, EdgeCreateView, ShortestRouteView

app_name = "routes"

urlpatterns = [
    path('nodes', NodeCreateView.as_view(), name='node-create'),
    path('edges', EdgeCreateView.as_view(), name='edge-create'),
    path('routes/shortest', ShortestRouteView.as_view(), name='route-shortest')
]