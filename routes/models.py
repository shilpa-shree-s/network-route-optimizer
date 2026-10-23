from django.db import models

# Create your models here.
class Node(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Edge(models.Model):
    source = models.ForeignKey(
        Node, on_delete=models.CASCADE, related_name="outgoing_edges"
    )
    destination = models.ForeignKey(
        Node, on_delete=models.CASCADE, related_name="incoming_edges"
    )
    latency = models.FloatField()

    class Meta:
        constraints = [  
            models.UniqueConstraint(
                fields=["source", "destination"], name="unique_edge"
            ),
        ]

    def __str__(self):
        return f"{self.source} -> {self.destination} ({self.latency})"