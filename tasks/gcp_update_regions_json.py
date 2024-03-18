#!/usr/bin/env python

# generate json files from GCP api

# UNPARSED_GCLOUD_JSON generated with:
# gcloud compute regions list --project <project> --format json

import json
from dataclasses import asdict

from django_model_classes import CloudAvailabilityZone, CloudProvider, CloudRegion
from constants import REGION_DATA_DIR, UNPARSED_GCLOUD_JSON
from get_cloud_region_short_names import get_gcp_slug

PROVIDER = "gcp"


def format_az_for_django_model(regions):
    """
    {
    "description": "africa-south1",
    "id": "1610",
    "kind": "compute#region",
    "name": "africa-south1",
    "zones": [
      "https://www.googleapis.com/compute/v1/projects/inner-bridge-296000/zones/africa-south1-b",
      "https://www.googleapis.com/compute/v1/projects/inner-bridge-296000/zones/africa-south1-a",
      "https://www.googleapis.com/compute/v1/projects/inner-bridge-296000/zones/africa-south1-c"
     ]
    },
    """
    formatted_azs = set()
    zone_id = None
    for region in regions:
        formatted_region = format_region_for_django_model([region])[0]
        for zone in sorted(region["zones"]):
            az_name = zone.split("/")[-1]  # africa-south1-b
            zone_letter = az_name.split("-")[-1]  # b
            az_short_name = (
                f"{formatted_region['region_short_name']}{zone_letter}"  # afs1b
            )
            region_pk = f"{PROVIDER}-{formatted_region['region_name']}"
            formatted_azs.add(
                CloudAvailabilityZone(
                    PROVIDER, region_pk, az_name, az_short_name, zone_id
                )
            )
    return [asdict(formatted) for formatted in formatted_azs]


def format_region_for_django_model(regions):
    formatted_regions = set()
    for region in regions:
        assert (
            region["kind"] == "compute#region"
        ), f"Sanity check - expected 'kind' to be 'compute#region', not {region['kind']}"
        name = region["name"]  # africa-south1
        short_name = get_gcp_slug(name)  # afs1
        region_model_data = CloudRegion(PROVIDER, name, short_name)
        formatted_regions.add(region_model_data)
    return [asdict(formatted) for formatted in formatted_regions]


def write_json_file(data, model):
    filename = REGION_DATA_DIR / f"{PROVIDER}_{model}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"file updated: {filename}")


def main():
    gcloud_regions = []
    with open(UNPARSED_GCLOUD_JSON, "r") as f:
        gcloud_regions = json.load(f)
    provider_model_data = [asdict(CloudProvider(PROVIDER))]
    az_model_data = format_az_for_django_model(gcloud_regions)
    region_model_data = format_region_for_django_model(gcloud_regions)

    assert (
        provider_model_data[0]["provider"] == PROVIDER
    ), f"Expected provider to be '{PROVIDER}', got {provider_model_data}"
    assert (
        len(region_model_data) > 15
    ), f"Expected at least 15 regions, got {len(region_model_data)}"
    assert (
        len(az_model_data) > 50
    ), f"Expected at least 50 availability zones, got {len(az_model_data)}"

    write_json_file(provider_model_data, "provider")
    write_json_file(region_model_data, "region")
    write_json_file(az_model_data, "az")


if __name__ == "__main__":
    main()
