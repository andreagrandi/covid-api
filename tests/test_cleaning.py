from covidapi.jh_cleaning.boat_map import map_boat_passengers
from covidapi.jh_cleaning.country_map import map_countries
from covidapi.jh_cleaning.county_admin2_map import (
    map_county_to_admin2,
    IGNORED_CITIES,
)
from covidapi.jh_cleaning.region_info import RegionNames as R


def test_unassigned_from_diamond_princess_is_diamond_princess_us():
    original = R(
        country_region="US",
        province_state="Unassigned Location (From Diamond Princess)",
        admin2=None,
    )
    expected = R(country_region="US", province_state="Diamond Princess", admin2=None)

    assert map_boat_passengers(original) == expected


def test_unassigned_from_diamond_princess_is_diamond_princess_canada():
    original = R(
        country_region="Canada",
        province_state="Unassigned Location (From Diamond Princess)",
        admin2=None,
    )
    expected = R(
        country_region="Canada", province_state="Diamond Princess", admin2=None
    )

    assert map_boat_passengers(original) == expected


def test_unassigned_from_grand_princess_is_grand_princess_canada():
    original = R(
        country_region="Canada",
        province_state="Grand Princess Cruise Ship",
        admin2=None,
    )
    expected = R(country_region="Canada", province_state="Grand Princess", admin2=None)

    assert map_boat_passengers(original) == expected


def test_cruise_ship_diamond_princess_is_diamond_princess():
    original = R(
        country_region="Cruise Ship", province_state="Diamond Princess", admin2=None,
    )
    expected = R(country_region="Diamond Princess", province_state=None, admin2=None)

    assert map_boat_passengers(original) == expected


def test_others_diamond_princess_is_diamond_princess():
    original = R(
        country_region="Others",
        province_state="Diamond Princess cruise ship",
        admin2=None,
    )
    expected = R(country_region="Diamond Princess", province_state=None, admin2=None)

    assert map_boat_passengers(original) == expected


def test_australia_from_diamond_princess_is_ignored():
    original = R(
        country_region="Australia", province_state="From Diamond Princess", admin2=None,
    )

    assert map_boat_passengers(original) is None


def test_us_city_from_diamond_princess_is_ignored():
    original = R(
        country_region="US",
        province_state="Lackland, TX (From Diamond Princess)",
        admin2=None,
    )

    assert map_boat_passengers(original) is None


def test_map_boat_passengers_ignores_normal_regions():
    original = R(country_region="US", province_state="California", admin2=None,)

    assert map_boat_passengers(original) == original


def test_map_countries_ignores_normal_regions():
    original = R(country_region="US", province_state="California", admin2=None,)

    assert map_countries(original) == original


def test_mainland_china_is_china():
    original = R(country_region="Mainland China", province_state="Hubei", admin2=None,)
    expected = R(country_region="China", province_state="Hubei", admin2=None,)
    assert map_countries(original) == expected


def test_china_special_administrative_regions_are_china_now():
    original = R(country_region="Hong Kong", province_state=None, admin2=None,)
    expected = R(country_region="China", province_state="Hong Kong", admin2=None,)
    assert map_countries(original) == expected

    original = R(country_region="Macau", province_state=None, admin2=None,)
    expected = R(country_region="China", province_state="Macau", admin2=None,)
    assert map_countries(original) == expected

    original = R(country_region="Macao", province_state=None, admin2=None,)
    expected = R(country_region="China", province_state="Macau", admin2=None,)
    assert map_countries(original) == expected


def test_south_korea_is_korea_south():
    original = R(country_region="South Korea", province_state=None, admin2=None,)
    expected = R(country_region="Korea, South", province_state=None, admin2=None,)
    assert map_countries(original) == expected


def test_the_the_countries_dont_have_the_the():
    original = R(country_region="The Bahamas", province_state=None, admin2=None,)
    expected = R(country_region="Bahamas", province_state=None, admin2=None,)
    assert map_countries(original) == expected

    original = R(country_region="Bahamas, The", province_state=None, admin2=None,)
    expected = R(country_region="Bahamas", province_state=None, admin2=None,)
    assert map_countries(original) == expected

    original = R(country_region="The Gambia", province_state=None, admin2=None,)
    expected = R(country_region="Gambia", province_state=None, admin2=None,)
    assert map_countries(original) == expected

    original = R(country_region="Gambia, The", province_state=None, admin2=None,)
    expected = R(country_region="Gambia", province_state=None, admin2=None,)
    assert map_countries(original) == expected


def test_shortening_official_country_names():
    original = R(country_region="Republic of Korea", province_state=None, admin2=None,)
    expected = R(country_region="Korea, South", province_state=None, admin2=None,)
    assert map_countries(original) == expected

    original = R(
        country_region="Iran (Islamic Republic of)", province_state=None, admin2=None,
    )
    expected = R(country_region="Iran", province_state=None, admin2=None,)
    assert map_countries(original) == expected

    original = R(
        country_region="Republic of Ireland", province_state=None, admin2=None,
    )
    expected = R(country_region="Ireland", province_state=None, admin2=None,)
    assert map_countries(original) == expected

    original = R(
        country_region="Republic of the Congo", province_state=None, admin2=None,
    )
    expected = R(country_region="Congo (Kinshasa)", province_state=None, admin2=None,)
    assert map_countries(original) == expected

    original = R(
        country_region="Republic of Moldova", province_state=None, admin2=None,
    )
    expected = R(country_region="Moldova", province_state=None, admin2=None,)
    assert map_countries(original) == expected

    original = R(country_region="Russian Federation", province_state=None, admin2=None,)
    expected = R(country_region="Russia", province_state=None, admin2=None,)
    assert map_countries(original) == expected

    original = R(country_region="Czech Republic", province_state=None, admin2=None,)
    expected = R(country_region="Czechia", province_state=None, admin2=None,)
    assert map_countries(original) == expected


def test_alternative_spellings():
    original = R(country_region="Viet Nam", province_state=None, admin2=None,)
    expected = R(country_region="Vietnam", province_state=None, admin2=None,)
    assert map_countries(original) == expected

    original = R(country_region="Cape Verde", province_state=None, admin2=None,)
    expected = R(country_region="Cabo Verde", province_state=None, admin2=None,)
    assert map_countries(original) == expected

    original = R(country_region="East Timor", province_state=None, admin2=None,)
    expected = R(country_region="Timor-Leste", province_state=None, admin2=None,)
    assert map_countries(original) == expected


def test_taiwan_has_an_asterisk_for_some_reason():
    original = R(country_region="Taiwan", province_state="Taiwan", admin2=None,)
    expected = R(country_region="Taiwan*", province_state=None, admin2=None,)
    assert map_countries(original) == expected


def test_countries_are_not_provinces_of_themselves():
    original = R(country_region="France", province_state="France", admin2=None,)
    expected = R(country_region="France", province_state=None, admin2=None,)
    assert map_countries(original) == expected

    original = R(country_region="UK", province_state="United Kingdom", admin2=None,)
    expected = R(country_region="United Kingdom", province_state=None, admin2=None,)
    assert map_countries(original) == expected


def test_countries_not_recognised_in_the_lookup_table_are_ignored():
    original = R(country_region="Palestine", province_state=None, admin2=None,)
    assert map_countries(original) is None

    original = R(
        country_region="occupied Palestinian territory",
        province_state=None,
        admin2=None,
    )
    assert map_countries(original) is None

    original = R(
        country_region="External territories", province_state=None, admin2=None,
    )
    assert map_countries(original) is None

    original = R(country_region="Guernsey", province_state=None, admin2=None,)
    assert map_countries(original) is None


def test_colonialism_happened():
    original = R(country_region="Guadaloupe", province_state=None, admin2=None,)
    expected = R(country_region="France", province_state="Guadeloupe", admin2=None,)
    assert map_countries(original) == expected

    original = R(country_region="Guadeloupe", province_state=None, admin2=None,)
    expected = R(country_region="France", province_state="Guadeloupe", admin2=None,)
    assert map_countries(original) == expected

    original = R(country_region="Greenland", province_state=None, admin2=None,)
    expected = R(country_region="Denmark", province_state="Greenland", admin2=None,)
    assert map_countries(original) == expected


def test_the_falklands_war_happened():
    original = R(
        country_region="United Kingdom",
        province_state="Falkland Islands (Islas Malvinas)",
        admin2=None,
    )
    expected = R(
        country_region="United Kingdom",
        province_state="Falkland Islands (Malvinas)",
        admin2=None,
    )
    assert map_countries(original) == expected


def test_no_matter_how_you_spell_saint_martin_it_is_not_independent_from_france():
    original = R(country_region="Saint Martin", province_state=None, admin2=None,)
    expected = R(country_region="France", province_state="St Martin", admin2=None,)
    assert map_countries(original) == expected

    original = R(country_region="St Martin", province_state=None, admin2=None,)
    expected = R(country_region="France", province_state="St Martin", admin2=None,)
    assert map_countries(original) == expected

    original = R(country_region="St. Martin", province_state=None, admin2=None,)
    expected = R(country_region="France", province_state="St Martin", admin2=None,)
    assert map_countries(original) == expected

    original = R(country_region="France", province_state="St. Martin", admin2=None,)
    expected = R(country_region="France", province_state="St Martin", admin2=None,)
    assert map_countries(original) == expected


def test_provinces_which_are_actully_cities_are_ignored():
    for city in IGNORED_CITIES:
        original = R(country_region="US", province_state=city, admin2=None)
        assert map_county_to_admin2(original) is None


def test_admin_areas_are_only_used_if_recognised_in_lookup_table():
    sterling_city = R(country_region="US", province_state="Alaska", admin2="Sterling")
    sterling_county = R(country_region="US", province_state="Texas", admin2="Sterling")
    sterling_county2 = R(
        country_region="US", province_state="Texas", admin2="Sterling County"
    )

    assert map_county_to_admin2(sterling_city) is None
    assert map_county_to_admin2(sterling_county) == sterling_county
    assert map_county_to_admin2(sterling_county2) == sterling_county


def test_unassigned_locations_are_ignored():
    original = R(country_region="US", province_state="California", admin2="unassigned")
    assert map_county_to_admin2(original) is None

    original = R(country_region="US", province_state="New York", admin2="Out-of-state")
    assert map_county_to_admin2(original) is None

    original = R(country_region="US", province_state="New York", admin2="Unknown")
    assert map_county_to_admin2(original) is None


def test_us_counties_do_not_include_county():
    original = R(
        country_region="US", province_state="California", admin2="Madera County"
    )
    expected = R(country_region="US", province_state="California", admin2="Madera")
    assert map_county_to_admin2(original) == expected
