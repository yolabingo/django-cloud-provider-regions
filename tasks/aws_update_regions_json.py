#!/usr/bin/env python

import json
from contextlib import closing
from dataclasses import asdict
import boto3

from django_model_classes import CloudAvailabilityZone, CloudProvider, CloudRegion
from constants import REGION_DATA_DIR

PROVIDER = "aws"

def fetch_azs():
    """Fetch all AWS availability zones in all regions"""
    azs = []
    with closing(boto3.client("ec2", region_name="us-east-1")) as client:
        region_names = [r["RegionName"] for r in client.describe_regions()["Regions"]]

    for region_name in region_names:
        with closing(boto3.client("ec2", region_name=region_name)) as client:
            azs += client.describe_availability_zones()["AvailabilityZones"]
    return azs


def format_az_for_django_model(azs):
    """
    AWS includes a 'ZoneId', which uses a number instead of a letter for zone designation
        {'GroupName': 'us-west-2',
        'Messages': [],
        'NetworkBorderGroup': 'us-west-2',
        'OptInStatus': 'opt-in-not-required',
        'RegionName': 'us-west-2',
        'State': 'available',
        'ZoneId': 'usw2-az2',
        'ZoneName': 'us-west-2b',
        'ZoneType': 'availability-zone'},
    """
    formatted_azs = set()
    for az in azs:
        assert (
            az["ZoneType"] == "availability-zone"
        ), f"Sanity check - ZoneType must be 'availability-zone', not {az['ZoneType']}"
        name = az["ZoneName"]  # us-west-2b
        zone_id = az["ZoneId"]  # usw2-az2
        zone_letter = az["ZoneName"][-1]  # b
        region_short_name = zone_id.split("-")[0]  # usw2
        short_name = f"{region_short_name}{zone_letter}"  # usw2b
        region = f"{PROVIDER}-{az['RegionName']}"
        formatted_azs.add(
            CloudAvailabilityZone(PROVIDER, region, name, short_name, zone_id)
        )
    return [asdict(formatted) for formatted in formatted_azs]


def format_region_for_django_model(azs):
    formatted_regions = set()
    for az in azs:
        name = az["RegionName"]
        short_name = az["ZoneId"].split("-")[0]
        region_model_data = CloudRegion(PROVIDER, name, short_name)
        formatted_regions.add(region_model_data)
    return [asdict(formatted) for formatted in formatted_regions]


def write_json_file(data, model):
    filename = REGION_DATA_DIR / f"{PROVIDER}_{model}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"file updated: {filename}")


def main():
    azs = fetch_azs()
    provider_model_data = [asdict(CloudProvider(PROVIDER))]
    az_model_data = format_az_for_django_model(azs)
    region_model_data = format_region_for_django_model(azs)

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
