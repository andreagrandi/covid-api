"""
Early reports contained city and county information reported using the "province_state" field.
Some of these are now reported in a reliable way using admin2.
Others are no longer reported individually.
This module maps the ones that can be mapped.
"""
from ..region_info import RegionNames

COUNTY_MAP = {
    "Santa Clara, CA": RegionNames(
        country_region="US", province_state="California", admin2="Santa Clara"
    ),
    "Santa Clara County, CA": RegionNames(
        country_region="US", province_state="California", admin2="Santa Clara"
    ),
    "Sacramento County, CA": RegionNames(
        country_region="US", province_state="California", admin2="Sacramento"
    ),
    "San Benito, CA": RegionNames(
        country_region="US", province_state="California", admin2="San Benito"
    ),
    "San Diego County, CA": RegionNames(
        country_region="US", province_state="California", admin2="San Diego"
    ),
    "Humboldt County, CA": RegionNames(
        country_region="US", province_state="California", admin2="Humboldt"
    ),
    "Los Angeles, CA": RegionNames(
        country_region="US", province_state="California", admin2="Los Angeles"
    ),
    "Orange, CA": RegionNames(
        country_region="US", province_state="California", admin2="Orange"
    ),
    "Orange County, CA": RegionNames(
        country_region="US", province_state="California", admin2="Orange"
    ),
    "Snohomish County, WA": RegionNames(
        country_region="US", province_state="Washington", admin2="Snohomish"
    ),
    "Providence, RI": RegionNames(
        country_region="US", province_state="Rhode Island", admin2="Providence"
    ),
    "King County, WA": RegionNames(
        country_region="US", province_state="Washington", admin2="King"
    ),
    "Cook County, IL": RegionNames(
        country_region="US", province_state="Illinois", admin2="Cook"
    ),
    "Grafton County, NH": RegionNames(
        country_region="US", province_state="New Hampshire", admin2="Grafton"
    ),
    "Hillsborough, FL": RegionNames(
        country_region="US", province_state="Florida", admin2="Hillsborough"
    ),
    "Placer County, CA": RegionNames(
        country_region="US", province_state="California", admin2="Placer"
    ),
    "San Mateo, CA": RegionNames(
        country_region="US", province_state="California", admin2="San Mateo"
    ),
    "Sarasota, FL": RegionNames(
        country_region="US", province_state="Florida", admin2="Sarasota"
    ),
    "Sonoma County, CA": RegionNames(
        country_region="US", province_state="California", admin2="Sonoma"
    ),
    "Umatilla, OR": RegionNames(
        country_region="US", province_state="Oregon", admin2="Umatilla"
    ),
    "New York City, NY": RegionNames(
        country_region="US", province_state="New York", admin2="New York City"
    ),
    "Fulton County, GA": RegionNames(
        country_region="US", province_state="Georgia", admin2="Fulton"
    ),
    "Washington County, OR": RegionNames(
        country_region="US", province_state="Oregon", admin2="Washington"
    ),
    " Norfolk County, MA": RegionNames(
        country_region="US", province_state="Massachusetts", admin2="Norfolk"
    ),
    "Norfolk County, MA": RegionNames(
        country_region="US", province_state="Massachusetts", admin2="Norfolk"
    ),
    "Maricopa County, AZ": RegionNames(
        country_region="US", province_state="Arizona", admin2="Maricopa"
    ),
    "Wake County, NC": RegionNames(
        country_region="US", province_state="North Carolina", admin2="Wake"
    ),
    "Westchester County, NY": RegionNames(
        country_region="US", province_state="New York", admin2="Westchester"
    ),
    "Bergen County, NJ": RegionNames(
        country_region="US", province_state="New Jersey", admin2="Bergen"
    ),
    "Harris County, TX": RegionNames(
        country_region="US", province_state="Texas", admin2="Harris"
    ),
    "San Francisco County, CA": RegionNames(
        country_region="US", province_state="California", admin2="San Francisco"
    ),
    "Clark County, NV": RegionNames(
        country_region="US", province_state="Nevada", admin2="Clark"
    ),
    "Contra Costa County, CA": RegionNames(
        country_region="US", province_state="California", admin2="Contra Costa"
    ),
    "Fort Bend County, TX": RegionNames(
        country_region="US", province_state="Texas", admin2="Fort Bend"
    ),
    "Grant County, WA": RegionNames(
        country_region="US", province_state="Washington", admin2="Grant"
    ),
    "Queens County, NY": RegionNames(
        country_region="US", province_state="New York", admin2="Queens"
    ),
    "Santa Rosa County, FL": RegionNames(
        country_region="US", province_state="Florida", admin2="Santa Rosa"
    ),
    "Williamson County, TN": RegionNames(
        country_region="US", province_state="Tennessee", admin2="Williamson"
    ),
    "New York County, NY": RegionNames(
        country_region="US", province_state="New York", admin2="New York City"
    ),  # This says NYC but it's NY county (FIPS 36061)
    "Montgomery County, MD": RegionNames(
        country_region="US", province_state="Maryland", admin2="Montgomery"
    ),
    "Suffolk County, MA": RegionNames(
        country_region="US", province_state="Massachusetts", admin2="Suffolk"
    ),
    "Denver County, CO": RegionNames(
        country_region="US", province_state="Colorado", admin2="Denver"
    ),
    "Summit County, CO": RegionNames(
        country_region="US", province_state="Colorado", admin2="Summit"
    ),
    "Chatham County, NC": RegionNames(
        country_region="US", province_state="North Carolina", admin2="Chatham"
    ),
    "Delaware County, PA": RegionNames(
        country_region="US", province_state="Pennsylvania", admin2="Delaware"
    ),
    "Douglas County, NE": RegionNames(
        country_region="US", province_state="Nebraska", admin2="Douglas"
    ),
    "Fayette County, KY": RegionNames(
        country_region="US", province_state="Kentucky", admin2="Fayette"
    ),
    "Floyd County, GA": RegionNames(
        country_region="US", province_state="Georgia", admin2="Floyd"
    ),
    "Marion County, IN": RegionNames(
        country_region="US", province_state="Indiana", admin2="Marion"
    ),
    "Middlesex County, MA": RegionNames(
        country_region="US", province_state="Massachusetts", admin2="Middlesex"
    ),
    "Nassau County, NY": RegionNames(
        country_region="US", province_state="New York", admin2="Nassau"
    ),
    "Ramsey County, MN": RegionNames(
        country_region="US", province_state="Minnesota", admin2="Ramsey"
    ),
    "Washoe County, NV": RegionNames(
        country_region="US", province_state="Nevada", admin2="Washoe"
    ),
    "Wayne County, PA": RegionNames(
        country_region="US", province_state="Pennsylvania", admin2="Wayne"
    ),
    "Yolo County, CA": RegionNames(
        country_region="US", province_state="California", admin2="Yolo"
    ),
    "Douglas County, CO": RegionNames(
        country_region="US", province_state="Colorado", admin2="Douglas"
    ),
    "Providence County, RI": RegionNames(
        country_region="US", province_state="Rhode Island", admin2="Providence"
    ),
    "Alameda County, CA": RegionNames(
        country_region="US", province_state="California", admin2="Alameda"
    ),
    "Montgomery County, PA": RegionNames(
        country_region="US", province_state="Pennsylvania", admin2="Montgomery"
    ),
    "Kershaw County, SC": RegionNames(
        country_region="US", province_state="South Carolina", admin2="Kershaw"
    ),
    "Pierce County, WA": RegionNames(
        country_region="US", province_state="Washington", admin2="Pierce"
    ),
    "Rockland County, NY": RegionNames(
        country_region="US", province_state="New York", admin2="Rockland"
    ),
    "Broward County, FL": RegionNames(
        country_region="US", province_state="Florida", admin2="Broward"
    ),
    "Cobb County, GA": RegionNames(
        country_region="US", province_state="Georgia", admin2="Cobb"
    ),
    "Johnson County, IA": RegionNames(
        country_region="US", province_state="Iowa", admin2="Johnson"
    ),
    "Fairfax County, VA": RegionNames(
        country_region="US", province_state="Virginia", admin2="Fairfax"
    ),
    "Harrison County, KY": RegionNames(
        country_region="US", province_state="Kentucky", admin2="Harrison"
    ),
    "Hendricks County, IN": RegionNames(
        country_region="US", province_state="Indiana", admin2="Hendricks"
    ),
    "Honolulu County, HI": RegionNames(
        country_region="US", province_state="Hawaii", admin2="Honolulu"
    ),
    "Jackson County, OR ": RegionNames(
        country_region="US", province_state="Oregon", admin2="Jackson"
    ),
    "Lee County, FL": RegionNames(
        country_region="US", province_state="Florida", admin2="Lee"
    ),
    "Manatee County, FL": RegionNames(
        country_region="US", province_state="Florida", admin2="Manatee"
    ),
    "Pinal County, AZ": RegionNames(
        country_region="US", province_state="Arizona", admin2="Pinal"
    ),
    "Saratoga County, NY": RegionNames(
        country_region="US", province_state="New York", admin2="Saratoga"
    ),
    "Washington, D.C.": RegionNames(
        country_region="US",
        province_state="District of Columbia",
        admin2="District of Columbia",
    ),
    "Bennington County, VT": RegionNames(
        country_region="US", province_state="Vermont", admin2="Bennington"
    ),
    "Berkshire County, MA": RegionNames(
        country_region="US", province_state="Massachusetts", admin2="Berkshire"
    ),
    "Carver County, MN": RegionNames(
        country_region="US", province_state="Minnesota", admin2="Carver"
    ),
    "Charleston County, SC": RegionNames(
        country_region="US", province_state="South Carolina", admin2="Charleston"
    ),
    "Charlotte County, FL": RegionNames(
        country_region="US", province_state="Florida", admin2="Charlotte"
    ),
    "Cherokee County, GA": RegionNames(
        country_region="US", province_state="Georgia", admin2="Cherokee"
    ),
    "Clark County, WA": RegionNames(
        country_region="US", province_state="Washington", admin2="Clark"
    ),
    "Collin County, TX": RegionNames(
        country_region="US", province_state="Texas", admin2="Collin"
    ),
    "Davidson County, TN": RegionNames(
        country_region="US", province_state="Tennessee", admin2="Davidson"
    ),
    "Davis County, UT": RegionNames(
        country_region="US", province_state="Utah", admin2="Davis"
    ),
    "Douglas County, OR": RegionNames(
        country_region="US", province_state="Oregon", admin2="Douglas"
    ),
    "El Paso County, CO": RegionNames(
        country_region="US", province_state="Colorado", admin2="El Paso"
    ),
    "Fairfield County, CT": RegionNames(
        country_region="US", province_state="Connecticut", admin2="Fairfield"
    ),
    "Fresno County, CA": RegionNames(
        country_region="US", province_state="California", admin2="Fresno"
    ),
    "Harford County, MD": RegionNames(
        country_region="US", province_state="Maryland", admin2="Harford"
    ),
    "Hudson County, NJ": RegionNames(
        country_region="US", province_state="New Jersey", admin2="Hudson"
    ),
    "Jefferson County, KY": RegionNames(
        country_region="US", province_state="Kentucky", admin2="Jefferson"
    ),
    "Jefferson County, WA": RegionNames(
        country_region="US", province_state="Washington", admin2="Jefferson"
    ),
    "Jefferson Parish, LA": RegionNames(
        country_region="US", province_state="Louisiana", admin2="Jefferson"
    ),
    "Johnson County, KS": RegionNames(
        country_region="US", province_state="Kansas", admin2="Johnson"
    ),
    "Kittitas County, WA": RegionNames(
        country_region="US", province_state="Washington", admin2="Kittitas"
    ),
    "Klamath County, OR": RegionNames(
        country_region="US", province_state="Oregon", admin2="Klamath"
    ),
    "Madera County, CA": RegionNames(
        country_region="US", province_state="California", admin2="Madera"
    ),
    "Marion County, OR": RegionNames(
        country_region="US", province_state="Oregon", admin2="Marion"
    ),
    "Okaloosa County, FL": RegionNames(
        country_region="US", province_state="Florida", admin2="Okaloosa"
    ),
    "Plymouth County, MA": RegionNames(
        country_region="US", province_state="Massachusetts", admin2="Plymouth"
    ),
    "Polk County, GA": RegionNames(
        country_region="US", province_state="Georgia", admin2="Polk"
    ),
    "Riverside County, CA": RegionNames(
        country_region="US", province_state="California", admin2="Riverside"
    ),
    "Rockingham County, NH": RegionNames(
        country_region="US", province_state="New Hampshire", admin2="Rockingham"
    ),
    "Shasta County, CA": RegionNames(
        country_region="US", province_state="California", admin2="Shasta"
    ),
    "Shelby County, TN": RegionNames(
        country_region="US", province_state="Tennessee", admin2="Shelby"
    ),
    "Spartanburg County, SC": RegionNames(
        country_region="US", province_state="South Carolina", admin2="Spartanburg"
    ),
    "Spokane County, WA": RegionNames(
        country_region="US", province_state="Washington", admin2="Spokane"
    ),
    "St. Louis County, MO": RegionNames(
        country_region="US", province_state="Missouri", admin2="St. Louis"
    ),
    "Suffolk County, NY": RegionNames(
        country_region="US", province_state="New York", admin2="Suffolk"
    ),
    "Tulsa County, OK": RegionNames(
        country_region="US", province_state="Oklahoma", admin2="Tulsa"
    ),
    "Ulster County, NY": RegionNames(
        country_region="US", province_state="New York", admin2="Ulster"
    ),
    "Volusia County, FL": RegionNames(
        country_region="US", province_state="Florida", admin2="Volusia"
    ),
    "Montgomery County, TX": RegionNames(
        country_region="US", province_state="Texas", admin2="Montgomery"
    ),
    "Santa Cruz County, CA": RegionNames(
        country_region="US", province_state="California", admin2="Santa Cruz"
    ),
}

IGNORED_CITIES = (
    "Toronto, ON",
    "Seattle, WA",
    "Chicago, IL",
    " Montreal, QC",
    "London, ON",
    "Boston, MA",
    "Madison, WI",
    "Portland, OR",
    "San Antonio, TX",
    "Tempe, AZ",
    "Berkeley, CA",
    "Unassigned Location, WA",
    "Unknown Location, MA",
    "Unassigned Location, VT",
    "Calgary, Alberta",
    "Edmonton, Alberta",
    "Wuhan Evacuee",
    "Norwell County, MA",
)

IGNORED_CITIES_ADMIN2 = (
    ("Brockton", "Massachusetts"),  # a city in Plymouth County
    ("Nashua", "New Hampshire"),  # a city in Hillsborough County
    ("Soldotna", "Alaska"),  # a city in Kenai Peninsula
    ("Sterling", "Alaska"),  # a city in Kenai Peninsula
)

IGNORED_ADMIN2 = (
    "unassigned",
    "Out-of-state",
    "Unknown",
)

ADMIN2_MAP = {
    "Doña Ana": "Dona Ana",
    "Desoto": "DeSoto",
    "LeSeur": "Le Sueur",
}


def clean_admin2(region_names):
    if region_names.admin2:
        admin2 = ADMIN2_MAP.get(region_names.admin2, region_names.admin2)
        province_state = region_names.province_state
        country_region = region_names.country_region

        if admin2 in IGNORED_ADMIN2:
            return None

        if (admin2, province_state) in IGNORED_CITIES_ADMIN2:
            return None

        if admin2.endswith(" County"):
            admin2 = admin2.replace(" County", "")

        return RegionNames(
            admin2=admin2, country_region=country_region, province_state=province_state
        )

    return region_names


def map_county_to_admin2(region_names):
    if region_names.province_state in IGNORED_CITIES:
        return None

    region_names = COUNTY_MAP.get(region_names.province_state, region_names)
    region_names = clean_admin2(region_names)

    return region_names
