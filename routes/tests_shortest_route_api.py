from rest_framework.test import APITestCase
from routes.models import Node, Edge, RouteQuery


class ShortestRouteTests(APITestCase):

    def setUp(self):
        # map: A --5-- B --1-- D, and A --2-- C --7-- D, and E alone
        self.a = Node.objects.create(name="A")
        self.b = Node.objects.create(name="B")
        self.c = Node.objects.create(name="C")
        self.d = Node.objects.create(name="D")
        self.e = Node.objects.create(name="E")

        Edge.objects.create(source=self.a, destination=self.b, latency=5)
        Edge.objects.create(source=self.a, destination=self.c, latency=2)
        Edge.objects.create(source=self.b, destination=self.d, latency=1)
        Edge.objects.create(source=self.c, destination=self.d, latency=7)

    def post_route(self, data):
        return self.client.post("/routes/shortest", data, format="json")

    def test_finds_shortest_route_returns_200(self):
        response = self.post_route({"source": "A", "destination": "D"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["total_latency"], 6)
        self.assertEqual(response.data["path"], ["A", "B", "D"])

    def test_no_path_returns_404(self):
        response = self.post_route({"source": "A", "destination": "E"})

        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.data)

    def test_unknown_node_returns_400(self):
        response = self.post_route({"source": "A", "destination": "Nope"})

        self.assertEqual(response.status_code, 400)

    def test_missing_destination_returns_400(self):
        response = self.post_route({"source": "A"})

        self.assertEqual(response.status_code, 400)

    def test_successful_search_is_saved_to_history(self):
        self.post_route({"source": "A", "destination": "D"})

        self.assertEqual(RouteQuery.objects.count(), 1)
        saved = RouteQuery.objects.first()
        self.assertEqual(saved.source, "A")
        self.assertEqual(saved.destination, "D")
        self.assertEqual(saved.path, ["A", "B", "D"])

    def test_failed_search_is_not_saved(self):
        self.post_route({"source": "A", "destination": "E"})

        self.assertEqual(RouteQuery.objects.count(), 0)