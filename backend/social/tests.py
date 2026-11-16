from django.urls import reverse
from rest_framework.test import APITestCase

class HealthEndpointTests(APITestCase):
    def test_health_is_public(self):
        response = self.client.get("/api/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "ok")
