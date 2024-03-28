#!/usr/bin/env python

import json

import constants

from django_cloud_provider_zones.models import (  # noqa: E402
    CloudProvider,
    CloudRegion,
    CloudAvailabilityZone,
)

CLOUD_PROVIDERS = ["aws", "gcp", "azu"]


def init_provider_db_from_json(provider_name):
    """
    Load cloud provider data from JSON files into the DJango database.
    """
    print(f"Loading provider data for {provider_name}")
    provider_data = constants.REGION_DATA_DIR / f"{provider_name}_provider.json"
    with open(provider_data) as fh:
        providers = json.load(fh)
        for p in providers:
            provider_instance, created = CloudProvider.objects.get_or_create(**p)
            if created:
                print(f"Created provider: {provider_name}")
            else:
                print(f"Provider already exists: {provider_name}")

    print(CloudProvider.objects.all())

    print("Loading region and availability zone data...")
    region_data = constants.REGION_DATA_DIR / f"{provider_name}_region.json"
    with open(region_data) as fh:
        regions = json.load(fh)
        for r in regions:
            r["provider"] = provider_instance
            region, created = CloudRegion.objects.get_or_create(**r)
            if created:
                print(f"Created region: {region}")
            else:
                print(f"Region already exists: {region}")

    print("CloudRegion.objects.all().count():")
    print(CloudRegion.objects.all().count())

    az_data = constants.REGION_DATA_DIR / f"{provider_name}_az.json"
    with open(az_data) as fh:
        for az in json.load(fh):
            az["region"] = CloudRegion.objects.get(
                original_region_name=az["original_region_name"], provider=provider_name
            )
            del az["original_region_name"]
            availability_zone, created = CloudAvailabilityZone.objects.get_or_create(
                **az,
            )
            if created:
                print(f"Saved availability zone: {availability_zone}")
            else:
                print(f"Availability zone already exists: {availability_zone}")

    print("CloudAvailabilityZone.objects.all().count():")
    print(CloudAvailabilityZone.objects.all().count())


def init_dbs_from_json():
    for provider in CLOUD_PROVIDERS:
        init_provider_db_from_json(provider)
