from enum import Enum, unique

@unique
class CardinalitySlug(Enum):
    central = "c"
    north = "n"
    south = "s"
    east = "e"
    west = "w"
    northeast = "ne"
    northwest = "nw"
    southeast = "se"
    southwest = "sw"


@unique
class GCPRegionBase(Enum):
    africa = "af"
    asia = "as"
    australia = "au"
    europe = "eu"
    me = "me"
    northamerica = "na"
    southamerica = "sa"
    us = "us"


def get_gcp_slug(region):
    """
    Convert GCP region to shorter unique slug
    "europe-west4" -> "euw4"
    """
    print(f"Converting '{region}' to GCP slug")
    region_base, cardinality = region.split("-")
    region_slug = GCPRegionBase[region_base].value
    # get cardinality and region number from 'west4'
    try:
        region_number = cardinality[-1:]
        cardinality_slug = CardinalitySlug[cardinality[:-1]].value
    except KeyError:
        # if the region number is two digits, europe-west10
        region_number = cardinality[-2:]
        cardinality_slug = CardinalitySlug[cardinality[:-2]].value
    region_slug += cardinality_slug + region_number
    if not (3 < len(region_slug) < 8):
        err = f"Invalid GCP slug: '{region_slug}' from '{region}'"
        raise ValueError(err)
    print(f"Converted '{region}' to '{region_slug}'")
    return region_slug
