"""
Several countries have been reported inconsistently.
This module maps country names to a canonical one defined in
https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/UID_ISO_FIPS_LookUp_Table.csv
"""
from .region_info import RegionNames

COUNTRY_MAP = {
    'Mainland China': 'China',
    'South Korea': 'Korea, South',
    'Taiwan': 'Taiwan*', # 🤷‍♂️
    'UK': 'United Kingdom',
    'Czech Republic': 'Czechia',
    'Bahamas, The': 'Bahamas',
    'The Bahamas': 'Bahamas',
    'Gambia, The': 'Gambia',
    'The Gambia': 'Gambia',
    'Republic of the Congo': 'Congo (Kinshasa)',
    'Viet Nam': 'Vietnam',
    'Russian Federation': 'Russia',
    'Republic of Moldova': 'Moldova',
    'Cape Verde': 'Cabo Verde',
    'East Timor': 'Timor-Leste',
    'Iran (Islamic Republic of)': 'Iran',
    'Republic of Korea': 'Korea, South',
    'Republic of Ireland': 'Ireland',
}

NOT_A_COUNTRY = {
    'Guadaloupe': 'France',
    'Guadeloupe': 'France',
    'Martinique': 'France',
    'Reunion': 'France',
    'French Guiana': 'France',
    'Saint Barthelemy': 'France',
    'St Martin': 'France',
    'St. Martin': 'France',
    'Saint Martin': 'France',
    'Mayotte': 'France',
    'Aruba': 'Netherlands',
    'Curacao': 'Netherlands',
    'Greenland': 'Denmark',
    'Faroe Islands': 'Denmark',
    'Hong Kong' : 'China',
    'Macau': 'China',
    'Macao': 'China',
    'Guam': 'US',
    'Puerto Rico': 'US',
    'Gibraltar': 'United Kingdom',
    'Cayman Islands': 'United Kingdom',
    'Channel Islands': 'United Kingdom',
}

IGNORED_TERRITORIES = (
    'Guernsey', # The lookup table does not distinguish between the channel islands
    'Jersey',
    'Palestine', # No longer recognised in the lookup table
    'occupied Palestinian territory',
    'Vatican City',
    'External territories', # not present in lookup table
    'Jervis Bay Territory', # not present in lookup table
)

PROVINCE_DUPLICATES_COUNTRY = (
    'Taiwan',
    'France',
    'United Kingdom',
    'Netherlands',
    'Denmark',
    'US',
    'UK',
)

PROVINCE_MAP = {
    "Fench Guiana": "French Guiana",
    "United States Virgin Islands": "Virgin Islands",
    "Virgin Islands, U.S.": "Virgin Islands",
    "Saint Martin": "St Martin",
    "St. Martin": "St Martin",
    "Macao": "Macau",
    "Falkland Islands (Islas Malvinas)": "Falkland Islands (Malvinas)",
    "Guadaloupe": "Guadeloupe",
}


def remove_sar(region_names):
    """
    e.g. Hong Kong SAR -> Hong Kong
    """
    return RegionNames(
        country_region = region_names.country_region.replace(' SAR', ''),
        province_state = region_names.province_state.replace(' SAR', '') if region_names.province_state else None,
        admin2 = region_names.admin2,
    )


def fix_fake_countries(region_names):
    """
    Handle provinces/states incorrectly reported as countries
    """
    if region_names.country_region in NOT_A_COUNTRY:
        return RegionNames(
            province_state = region_names.country_region,
            country_region = NOT_A_COUNTRY[region_names.country_region],
            admin2 = region_names.admin2
        )

    return region_names


def fix_fake_provinces(region_names):
    """
    Handle countries/regions incorrectly reported as provinces (according to the lookup table)
    """
    if region_names.province_state in PROVINCE_DUPLICATES_COUNTRY:
        return RegionNames(
            country_region = 'Taiwan' if region_names.province_state == 'Taiwan' else region_names.country_region,
            province_state = None,
            admin2 = None
        )

    return region_names


def correct_typos(region_names):
    """
    Map countries and provinces to canonical names.
    """
    country_region = COUNTRY_MAP.get(region_names.country_region, region_names.country_region)

    province_state = region_names.province_state
    if province_state:
        province_state = PROVINCE_MAP.get(province_state, province_state)

    return RegionNames(
        province_state = province_state,
        country_region = country_region,
        admin2 = region_names.admin2
    )

def map_countries(region_names):
    if region_names.country_region in IGNORED_TERRITORIES:
        return None

    region_names = remove_sar(region_names)
    region_names = fix_fake_countries(region_names)
    region_names = fix_fake_provinces(region_names)
    region_names = correct_typos(region_names)

    return region_names
