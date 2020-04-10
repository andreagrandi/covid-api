from typing import NamedTuple, Optional
from ..schemas.enums import Scope


class RegionNames(NamedTuple):
    """
    A set of region names that may be matched to an IdentifiedRegion
    """
    admin2: Optional[str]
    province_state: Optional[str]
    country_region: str

    @staticmethod
    def parse_from_lookup_table(record):
        admin2 = record['Admin2']
        province_state = record['Province_State']

        return RegionNames(
            admin2 = admin2 if admin2 else None,
            province_state = province_state if province_state else None,
            country_region = record['Country_Region'],
        )

    @staticmethod
    def parse_from_report(record):
        admin2 = record.get('Admin2')
        province_state = record.get('Province_State') or record.get('Province/State')
        country_region = record.get('Country_Region') or record['Country/Region']

        return RegionNames(
            admin2 = admin2 if admin2 else None,
            province_state = province_state if province_state else None,
            country_region = country_region,
        )

    @property
    def scope(self):
        if self.admin2:
            return Scope.ADMIN2
        elif self.province_state:
            return Scope.PROVINCE_STATE
        else:
            return Scope.COUNTRY_REGION


class LatLong(NamedTuple):
    """
    A geographic coordinate
    """
    latitude: float
    longitude: float

    @staticmethod
    def parse_from_lookup_table(record):
        try:
            latitude = float(record['Lat'])
            longitude = float(record['Long_'])
        except ValueError:
            return None
        else:
            return LatLong(latitude=latitude, longitude=longitude)


class IdentifiedRegion(NamedTuple):
    """
    A region that:

    - has a unique identifier
    - is matched to a country code, and optionally a FIPS code (US)
    - is classified as country/region, province/state, or admin2
    """
    uid: int
    fips: Optional[str]
    iso2: str
    iso3: str
    scope: Scope

    @staticmethod
    def parse_from_lookup_table(record, scope):
        fips = record['FIPS']

        return IdentifiedRegion(
            fips = fips if fips else None,
            iso2 = record['iso2'],
            iso3 = record['iso3'],
            uid = int(record['UID']),
            scope = scope
        )


class RegionInfo(NamedTuple):
    """
    Everything we know about a region
    """
    identified_region: IdentifiedRegion
    region_names: RegionNames
    population: Optional[int]
    combined_key: str
    coordinates: Optional[LatLong]

    @staticmethod
    def parse_from_lookup_table(record):
        combined_key = record['Combined_Key']
        region_names = RegionNames.parse_from_lookup_table(record)
        identified_region = IdentifiedRegion.parse_from_lookup_table(record, region_names.scope)
        population = int(record['Population']) if record['Population'] else None

        return RegionInfo(
            identified_region=identified_region,
            region_names=region_names,
            population=population,
            combined_key=combined_key,
            coordinates = LatLong.parse_from_lookup_table(record)
        )
