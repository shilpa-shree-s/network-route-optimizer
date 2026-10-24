from rest_framework.test import APITestCase
from routes.models import Node, Edge


class EdgeCreateTests(APITestCase):

    def setUp(self):
        Node.objects.create(name="ServerA")
        Node.objects.create(name="ServerB")

    def post_edge(self, data):
        return self.client.post("/edges", data, format="json")

    def test_create_edge_returns_201(self):
        response = self.post_edge(
            {"source": "ServerA", "destination": "ServerB", "latency": 12.5}
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["source"], "ServerA")
        self.assertEqual(Edge.objects.count(), 1)

    def test_missing_source_returns_400(self):
        response = self.post_edge({"destination": "ServerB", "latency": 5})
        self.assertEqual(response.status_code, 400)

    def test_zero_latency_returns_400(self):
        response = self.post_edge(
            {"source": "ServerA", "destination": "ServerB", "latency": 0}
        )
        self.assertEqual(response.status_code, 400)

    def test_unknown_node_returns_400(self):
        response = self.post_edge(
            {"source": "ServerA", "destination": "Nope", "latency": 5}
        )
        self.assertEqual(response.status_code, 400)

    def test_duplicate_edge_returns_400(self):
        self.post_edge({"source": "ServerA", "destination": "ServerB", "latency": 5})
        response = self.post_edge(
            {"source": "ServerA", "destination": "ServerB", "latency": 7}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Edge.objects.count(), 1)

    def test_reverse_edge_counts_as_duplicate(self):
        self.post_edge({"source": "ServerA", "destination": "ServerB", "latency": 5})
        response = self.post_edge(
            {"source": "ServerB", "destination": "ServerA", "latency": 5}
        )
        self.assertEqual(response.status_code, 400)