from django.urls import path
from .views import NodeCreateView

app_name = "routes"

urlpatterns = [
    path('nodes', NodeCreateView.as_view(), name='node-create')
]