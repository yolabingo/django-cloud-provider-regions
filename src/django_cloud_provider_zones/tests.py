import json

from django.test import Client, TestCase
from django.test.utils import override_settings

from django_cloud_provider_zones import urls


@override_settings(
    ROOT_URLCONF=urls,
    INSTALLED_APPS=[
        "django.contrib.contenttypes",
        "rest_framework",
        "django_cloud_provider_zones",
    ],
)
class CloudProviderTestCase(TestCase):
    fixtures = ["django_cloud_provider_zones.json"]

    def setUp(self):
        self.client = Client()

    def test_cloud_provider_name(self):
        providers = [{"provider": "aws"}, {"provider": "gcp"}]
        response = self.client.get("/cloud-providers/")
        self.assertEqual(response.status_code, 200)
        response_dict = json.loads(response.content.decode("utf-8"))
        for provider in providers:
            self.assertIn(provider, response_dict)

    def test_region_fixture_data(self):
        """simple sanity check"""
        expected_regions = [
            {
                "provider": "gcp",
                "record_last_synced": "2024-03-18",
                "region_name": "us-west4",
                "region_name_with_provider": "gcp-us-west4",
                "region_short_name": "usw4",
                "region_short_name_with_provider": "gcpusw4",
            },
            {
                "provider": "aws",
                "region_name": "ap-northeast-3",
                "region_short_name": "apne3",
                "region_name_with_provider": "aws-ap-northeast-3",
                "region_short_name_with_provider": "awsapne3",
                "record_last_synced": "2024-03-17",
            },
        ]
        response = self.client.get("/cloud-regions/")
        self.assertEqual(response.status_code, 200)
        response_dict = json.loads(response.content.decode("utf-8"))
        for region in expected_regions:
            self.assertIn(region, response_dict)

    def test_availability_zone_fixture_data(self):
        expected_zones = [
            {
                "provider": "gcp",
                "region": "gcp-southamerica-east1",
                "az_name": "southamerica-east1-b",
                "az_short_name": "sae1b",
                "az_id": None,
                "az_name_with_provider": "gcp-southamerica-east1-b",
                "az_short_name_with_provider": "gcpsae1b",
                "record_last_synced": "2024-03-18",
            },
            {
                "provider": "aws",
                "region": "aws-ap-northeast-1",
                "az_name": "ap-northeast-1c",
                "az_short_name": "apne1c",
                "az_id": "apne1-az1",
                "az_name_with_provider": "aws-ap-northeast-1c",
                "az_short_name_with_provider": "awsapne1c",
                "record_last_synced": "2024-03-17",
            },
        ]
        response = self.client.get("/cloud-availability-zones/")
        response_dict = json.loads(response.content.decode("utf-8"))
        for zone in expected_zones:
            self.assertIn(zone, response_dict)
