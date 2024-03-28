from dataclasses import dataclass
from datetime import datetime

TODAY = datetime.now().strftime("%Y-%m-%d")


@dataclass(frozen=True)
class CloudProvider:
    provider: str  # Django Primary Key


@dataclass(frozen=True)
class CloudRegion:
    """
    frozen=True makes the class hashable which allows using set() to remove duplicates
    """

    geographic_region: str
    cardinality: str
    number: str
    original_region_name: str


@dataclass(frozen=True)
class CloudAvailabilityZone:
    """
    frozen=True makes the class hashable which allows using set() to remove duplicates
    """

    original_region_name: str
    original_az_name: str
    az: str
