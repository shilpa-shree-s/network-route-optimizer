from rest_framework.test import APITestCase
from routes.models import Node


class NodeCreateTests(APITestCase):

    def test_create_node_returns_201(self):
        response = self.client.post("/nodes", {"name": "ServerA"}, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "ServerA")
        self.assertIn("id", response.data)
        self.assertEqual(Node.objects.count(), 1)

    def test_missing_name_returns_400(self):
        response = self.client.post("/nodes", {}, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Node.objects.count(), 0)

    def test_duplicate_name_returns_400(self):
        Node.objects.create(name="ServerA")

        response = self.client.post("/nodes", {"name": "ServerA"}, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Node.objects.count(), 1)