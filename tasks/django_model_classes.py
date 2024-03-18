from dataclasses import dataclass, field
from datetime import datetime

TODAY = datetime.now().strftime("%Y-%m-%d")


@dataclass(frozen=True)
class CloudProvider:
    provider: str  # Django Primary Key


@dataclass(frozen=True)
class CloudRegionBase:
    """
    Base class permits properties on the child classes
    frozen=True makes the class hashable which allows using set() to remove duplicates
    """

    provider: str
    region_name: str
    region_short_name: str
    region_name_with_provider: str = field(init=False)  # Django Primary Key
    region_short_name_with_provider: str = field(init=False)
    record_last_synced: str = field(init=False)


class CloudRegion(CloudRegionBase):
    region_name: str
    region_short_name: str

    @property
    def region_name_with_provider(self):
        return f"{self.provider}-{self.region_name}"

    @property
    def region_short_name_with_provider(self):
        return f"{self.provider}{self.region_short_name}"

    @property
    def record_last_synced(self):
        return TODAY


@dataclass(frozen=True)
class CloudAvailabilityZoneBase:
    """
    Base class permits properties on the child classes
    frozen=True makes the class hashable which allows using set() to remove duplicates
    """

    provider: str
    region: str
    az_name: str
    az_short_name: str
    az_id: str | None
    az_name_with_provider: str = field(init=False)
    az_short_name_with_provider: str = field(init=False)
    record_last_synced: str = field(init=False)


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
    region: str
    az_name: str
    az_short_name: str
    az_id: str | None

    @property
    def az_name_with_provider(self):
        return f"{self.provider}-{self.az_name}"

    @property
    def az_short_name_with_provider(self):
        return f"{self.provider}{self.az_short_name}"

    @property
    def record_last_synced(self):
        return TODAY
