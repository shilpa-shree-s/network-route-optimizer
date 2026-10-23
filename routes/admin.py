from django.contrib import admin
from .models import Node, Edge, RouteQuery

# Register your models here.
admin.site.register(Node)
admin.site.register(Edge)
admin.site.register(RouteQuery)