from covidapi.jh_cleaning.region_info import RegionNames


def map_boat_passengers(region_match):
    united_federation_of_cruise_ships = (
        'Cruise Ship',
        'Others',
    )

    diamond_princess = (
        'Diamond Princess',
        'Diamond Princess cruise ship',
    )

    diamond_princess_to_country = (
        'Unassigned Location (From Diamond Princess)',
        'From Diamond Princess' # used for Australia, but this isn't included in the lookup table
    )

    grand_princess_to_country = (
        'Grand Princess Cruise Ship',
    )

    diamond_princess_to_city = (
        'Lackland, TX (From Diamond Princess)',
        'Omaha, NE (From Diamond Princess)',
        'Travis, CA (From Diamond Princess)',
    )

    if region_match.country_region in ('US', 'Canada') and region_match.province_state in diamond_princess_to_country:
            return RegionNames(
                country_region = region_match.country_region,
                province_state = 'Diamond Princess',
                admin2 = None
            )
    elif region_match.country_region in ('US', 'Canada') and region_match.province_state in grand_princess_to_country:
            return RegionNames(
                country_region = region_match.country_region,
                province_state = 'Grand Princess',
                admin2 = None
            )
    elif (region_match.province_state in diamond_princess) and (region_match.country_region in united_federation_of_cruise_ships):
        # The Diamond Princess got promoted from a province into a country
        return RegionNames(
            country_region='Diamond Princess',
            province_state=None,
            admin2 = None
        )
    elif (
            region_match.province_state in diamond_princess_to_country
            or region_match.province_state in diamond_princess_to_city
        ):
        return None

    return region_match
