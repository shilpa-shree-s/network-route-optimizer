from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase

from routes.models import RouteQuery


class RouteHistoryTests(APITestCase):

    def setUp(self):
        RouteQuery.objects.create(
            source="A", destination="D", total_latency=6, path=["A", "B", "D"]
        )
        RouteQuery.objects.create(
            source="B", destination="C", total_latency=3, path=["B", "C"]
        )
        RouteQuery.objects.create(
            source="A", destination="C", total_latency=2, path=["A", "C"]
        )

    def get_history(self, params=None):
        return self.client.get("/routes/history", params or {})

    def test_returns_all_records_with_200(self):
        response = self.get_history()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_newest_record_comes_first(self):
        response = self.get_history()

        self.assertEqual(response.data[0]["destination"], "C")
        self.assertEqual(response.data[0]["source"], "A")

    def test_response_has_expected_fields(self):
        response = self.get_history()

        expected = {"id", "source", "destination", "total_latency", "path", "created_at"}
        self.assertEqual(set(response.data[0].keys()), expected)

    def test_filter_by_source(self):
        response = self.get_history({"source": "A"})

        self.assertEqual(len(response.data), 2)
        for record in response.data:
            self.assertEqual(record["source"], "A")

    def test_filter_by_destination(self):
        response = self.get_history({"destination": "C"})

        self.assertEqual(len(response.data), 2)

    def test_limit(self):
        response = self.get_history({"limit": 1})

        self.assertEqual(len(response.data), 1)

    def test_invalid_limit_returns_400(self):
        response = self.get_history({"limit": "abc"})

        self.assertEqual(response.status_code, 400)

    def test_invalid_date_returns_400(self):
        response = self.get_history({"date_from": "not-a-date"})

        self.assertEqual(response.status_code, 400)

    def test_date_from_in_future_returns_empty_list(self):
        tomorrow = (timezone.now() + timedelta(days=1)).isoformat()

        response = self.get_history({"date_from": tomorrow})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_date_to_in_past_returns_empty_list(self):
        yesterday = (timezone.now() - timedelta(days=1)).isoformat()

        response = self.get_history({"date_to": yesterday})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])