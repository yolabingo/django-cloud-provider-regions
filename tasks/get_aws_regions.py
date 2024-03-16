from contextlib import closing
from dataclasses import asdict
from pprint import pprint

import boto3

from django_model_classes import CloudProvider, CloudAvailabilityZone

def get_azs():
    azs = []
    with closing(boto3.client('ec2', region_name='us-east-1')) as client:
        region_names = [r['RegionName'] for r in client.describe_regions()['Regions']]

    for region_name in region_names:
        with closing(boto3.client('ec2', region_name=region_name)) as client:
            azs += client.describe_availability_zones()['AvailabilityZones']
    print(f"Length of azs: {len(azs)}   ")
    return azs

def format_az_as_django_model(az):
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
    assert az["ZoneType"] == "availability-zone", f"Sanity check - ZoneType must be 'availability-zone', not {az['ZoneType']}"
    name = az['ZoneName'] # us-west-2b
    zone_id = az["ZoneId"] # usw2-az2
    zone_letter = az['ZoneName'][-1]  # b
    region_short_name = zone_id.split('-')[0] # usw2
    short_name = f"{region_short_name}{zone_letter}" # usw2b
    az_model_data = CloudAvailabilityZone( "aws", name, short_name, zone_id)
    pprint(az_model_data)
    return asdict(az_model_data)

azs = get_azs()

provider_model_data = CloudProvider('aws')
az_model_data = [format_az_as_django_model(az) for az in azs] 
pprint(az_model_data)
