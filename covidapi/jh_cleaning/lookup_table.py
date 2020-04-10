import requests
import csv
from .county_admin2_map import map_county_to_admin2
from .country_map import map_countries
from .boat_map import map_boat_passengers
from .region_info import RegionInfo


class Matcher():
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
        """
        try:
            return self.region_matches[region_match]
        except KeyError:
            # Region names are not used consistently, so account for some
            # inconsistencies before trying the lookup
            fuzzy = map_countries(region_match)
            fuzzier = map_county_to_admin2(fuzzy) if fuzzy else None
            fuzziest = map_boat_passengers(fuzzier) if fuzzier else None

            try:
                return self.region_matches[fuzziest] if fuzziest else None
            except KeyError:
                print(fuzziest)
                raise

    def lookup_by_id(self, uid):
        """
        Lookup by the ID JH provide in the lookup table
        """
        return self.by_id[uid]

    def __iter__(self):
        return iter(self.by_id.values())

    def _fetch(self):
        url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/UID_ISO_FIPS_LookUp_Table.csv'
        response = requests.get(url)
        response.raise_for_status()

        csv_reader = csv.DictReader((line.decode('utf8') for line in response.iter_lines()))

        for record in csv_reader:
            try:
                region_info = RegionInfo.parse_from_lookup_table(record)

                self.region_matches[region_info.region_names] = region_info
                self.key_matches[region_info.combined_key] = region_info
                self.by_id[region_info.identified_region.uid] = region_info
            except KeyError:
                print(record)
                raise
