#!/usr/bin/env python

import json

import constants

from django_cloud_provider_zones.models import (  # noqa: E402
    CloudProvider,
    CloudRegion,
    CloudAvailabilityZone,
)


def init_provider_db_from_json(cloud_provider):
    """
    Load cloud provider data from JSON files into the DJango database.
    """
    print(f"Loading provider data for {cloud_provider}")
    provider_data = constants.REGION_DATA_DIR / f"{cloud_provider}_provider.json"
    with open(provider_data) as fh:
        providers = json.load(fh)
        for p in providers:
            provider = CloudProvider(**p)
            provider.save()

    print(CloudProvider.objects.all())

    print("Loading region and availability zone data...")
    region_data = constants.REGION_DATA_DIR / f"{cloud_provider}_region.json"
    with open(region_data) as fh:
        provider = CloudProvider.objects.get(provider=cloud_provider)
        regions = json.load(fh)
        for r in regions:
            r["provider"] = provider
            region = CloudRegion(**r)
            region.save()

    print("CloudRegion.objects.all().count():")
    print(CloudRegion.objects.all().count())

    az_data = constants.REGION_DATA_DIR / f"{cloud_provider}_az.json"
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


def init_dbs_from_json():
    for provider in constants.CLOUD_PROVIDERS:
        init_provider_db_from_json(provider)
