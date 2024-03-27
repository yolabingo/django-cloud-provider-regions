#!/usr/bin/env python

import json
from contextlib import closing
import boto3

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

def write_json_file(data, model):
    filename = REGION_DATA_DIR / f"{PROVIDER}_{model}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"file updated: {filename}")


def main():
    azs = fetch_azs()
    write_json_file(azs, "unprocessed")

if __name__ == "__main__":
    main()
