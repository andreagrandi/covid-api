import requests
import csv
from .county_admin2_map import map_county_to_admin2
from .country_map import map_countries
from .boat_map import map_boat_passengers
from ..region_info import RegionInfo


def canonical_location(region_match):
    """
    Region names are not used consistently, so account for some inconsistencies

    None = just ignore this location
    """
    region_match = map_countries(region_match)
    region_match = map_county_to_admin2(region_match) if region_match else None
    return map_boat_passengers(region_match) if region_match else None


class Matcher:
    """
    Maps a daily report to a canonical region from the lookup table
    (https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/UID_ISO_FIPS_LookUp_Table.csv)
    """

    def __init__(self):
        self.region_matches = {}
        self.key_matches = {}
        self.by_id = {}
        self._fetch()

    def match_region(self, region_match):
        """
        Attempt to lookup a region using the names provided

        None = just ignore this region
        """
        try:
            return self.region_matches[region_match]
        except KeyError:
            region_match = canonical_location(region_match)

            return self.region_matches[region_match] if region_match else None

    def lookup_by_id(self, uid):
        """
        Lookup by the ID JH provide in the lookup table
        """
        return self.by_id[uid]

    def __iter__(self):
        return iter(self.by_id.values())

    def _fetch(self):
        url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/UID_ISO_FIPS_LookUp_Table.csv"
        response = requests.get(url)
        response.raise_for_status()

        csv_reader = csv.DictReader(
            (line.decode("utf8") for line in response.iter_lines())
        )

        for record in csv_reader:
            try:
                region_info = RegionInfo.parse_from_lookup_table(record)

                self.region_matches[region_info.region_names] = region_info
                self.key_matches[region_info.combined_key] = region_info
                self.by_id[region_info.identified_region.uid] = region_info
            except KeyError:
                print(record)
                raise
