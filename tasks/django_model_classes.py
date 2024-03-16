import re
from dataclasses import dataclass, field

# Format Cloud Provider, Region, and Availability Zone names for Django model classes
short_name_regex = re.compile(r"^[a-z0-9]{3,}$")

@dataclass
class CloudProvider:
    def __init__(self, name: str):
        self.provider = name
        assert short_name_regex.match(self.provider), f"CloudProvider name must match {short_name_regex.pattern}"

@dataclass
class CloudRegion:
    def __init__(self, provider, region_name: str, region_short_name: str):
        self.provider = provider
        self.region_name = region_name
        self.region_name_with_provider = f"{provider}-{region_name}"
        self.region_short_name = region_short_name
        self.region_short_name_with_provider = f"{provider}{region_short_name}"

        assert short_name_regex.match(self.provider), f"CloudRegion provider must match {short_name_regex.pattern}"
        assert short_name_regex.match(self.region_short_name), "CloudRegion region_short_name must match {short_name_regex.pattern}"
        assert short_name_regex.match(self.region_short_name_with_provider), "CloudRegion region_short_name_with_provider must match {short_name_regex.pattern}"

@dataclass
class CloudAvailabilityZoneBase:
    """
    This allows asdict() to work for 
    """
    provider: str
    az_name: str
    az_short_name: str
    az_id: str | None
    az_name_with_region: str = field(init=False)
    az_short_name_with_region: str = field(init=False)

class CloudAvailabilityZone(CloudAvailabilityZoneBase):
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
    provider: str
    az_name: str
    az_short_name: str
    az_id: str | None

    @property
    def az_name_with_region(self):
        return f"{self.provider}-{self.az_name}"
    
    @property
    def az_short_name_with_region(self):
        return f"{self.provider}{self.az_short_name}"
    