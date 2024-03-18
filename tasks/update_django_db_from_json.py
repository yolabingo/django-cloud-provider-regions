#!/usr/bin/env python

import json

from django.core.management import call_command

from constants import APP_NAME, CLOUD_PROVIDERS, REGION_DATA_DIR, FIXTURES_DIR
from boot_django import boot_django

boot_django()
from django_cloud_provider_zones.models import (  # noqa: E402
    CloudProvider,
    CloudRegion,
    CloudAvailabilityZone,
)


def init_db_from_json(cloud_provider):
    """
    Load cloud provider data from JSON files into the DJango database.
    """
    print(f"Loading provider data for {cloud_provider}")
    provider_data = REGION_DATA_DIR / f"{cloud_provider}_provider.json"
    with open(provider_data) as fh:
        providers = json.load(fh)
        for p in providers:
            provider = CloudProvider(**p)
            provider.save()

    print(CloudProvider.objects.all())

    print("Loading region and availability zone data...")
    region_data = REGION_DATA_DIR / f"{cloud_provider}_region.json"
    with open(region_data) as fh:
        provider = CloudProvider.objects.get(provider=cloud_provider)
        regions = json.load(fh)
        for r in regions:
            r["provider"] = provider
            region = CloudRegion(**r)
            region.save()

    print("CloudRegion.objects.all().count():")
    print(CloudRegion.objects.all().count())

    az_data = REGION_DATA_DIR / f"{cloud_provider}_az.json"
    with open(az_data) as fh:
        provider = CloudProvider.objects.get(provider=cloud_provider)
        azs = json.load(fh)
        for az in azs:
            az["provider"] = provider
            az["region"] = CloudRegion.objects.get(
                region_name_with_provider=az["region"]
            )
            availability_zone = CloudAvailabilityZone(**az)
            availability_zone.save()

    print("CloudAvailabilityZone.objects.all().count():")
    print(CloudAvailabilityZone.objects.all().count())


def create_fixture():
    """Create Django fixture from the loaded data"""
    fixture_file = (FIXTURES_DIR / f"{APP_NAME}.json",)
    call_command(
        "dumpdata",
        "--format",
        "json",
        "--indent",
        "4",
        "--output",
        fixture_file,
        APP_NAME,
    )
    print(f"Fixture created: {str(fixture_file)}")


def main():
    print("makemigrations")
    call_command("makemigrations", APP_NAME)
    print("migrate")
    call_command("migrate")
    print("Load data from JSON files...")
    for cloud_provider in CLOUD_PROVIDERS:
        init_db_from_json(cloud_provider)
    print("Create fixture")
    create_fixture()


if __name__ == "__main__":
    main()
