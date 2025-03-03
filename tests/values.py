import os
from dotenv import load_dotenv


__current_script_path_file = os.path.abspath(__file__)
path_to_root_of_project = __current_script_path_file[
    : __current_script_path_file.find("/tests/")
]
geoloc_util_location = path_to_root_of_project + "/geolocutil.py"
load_dotenv(path_to_root_of_project + "/.env")

HELP_MESSAGE = """usage: geolocutil.py [-h] [-p] [-j] [-e] locations [locations ...]

Retrieves geolocation data utilizing Open Weather Geocoding API

positional arguments:
  locations     A list of locations ("City, ST" or zip code in 5 digit format "12345") - US Cities and Zip codes only.
                Examples:
                	'Madison, WI'
                	'12345'
                	'Madison, WI' '12345' 'Chicago, IL' '10001'

options:
  -h, --help    show this help message and exit
  -p, --print   Outputs pretty print to stdout instead of json string
  -j, --json    Converts all strings to ascii in json output
  -e, --errors  Prints out Error messages to stdout
"""

SKIPPED_MESSAGE = "Any queries not included was skipped due to an error.  Please use `-e` in the function call to include errors in the output."

VALID_NY_NY = {"name": "New York", "lat": 40.7127281, "lon": -74.0060152}

VALID_MADISON_WI = {"name": "Madison", "lat": 43.074761, "lon": -89.3837613}

VALID_CHICAGO_IL = {"name": "Chicago", "lat": 41.8755616, "lon": -87.6244212}

VALID_LOS_ANGELES_CA = {"name": "Los Angeles", "lat": 34.0536909, "lon": -118.242766}

VALID_SAN_JUAN_PR = {"name": "San Juan", "lat": 18.465299, "lon": -66.116666}

VALID_HAGATNA = {"name": "Hagåtña", "lat": 13.4748148, "lon": 144.7516191}

VALID_12345 = {
    "name": "Schenectady",
    "lat": 42.8142,
    "lon": -73.9396,
}

VALID_10001 = {
    "name": "New York",
    "lat": 40.7484,
    "lon": -73.9967,
}

VALID_00501 = {
    "name": "Suffolk County",
    "lat": 40.8154,
    "lon": -73.0451,
}

VALID_00901 = {
    "name": "Río Piedras",
    "lat": 18.4663,
    "lon": -66.1057,
}

VALID_96913 = {
    "name": "Mangilau Municipality",
    "lat": 13.4443,
    "lon": 144.7863,
}

NO_VALIDS: list = []

LINE_SPLIT = "|-------------------------------------------------------------------------------------|"

HEADER = "| Search Term               | City/Town Name            | Latitude     | Longitude    |"

VALID_MADISON_WI_P_FLAG = "| Madison, WI               | Madison                   | 43.074761    | -89.3837613  |"
VALID_12345_P_FLAG = "| 12345                     | Schenectady               | 42.8142      | -73.9396     |"

VALID_MULTIPLE_P_FLAG = f"""|-------------------------------------------------------------------------------------|
| Search Term               | City/Town Name            | Latitude     | Longitude    |
|-------------------------------------------------------------------------------------|
| Madison WI                | Madison                   | 43.074761    | -89.3837613  |
| 12345                     | Schenectady               | 42.8142      | -73.9396     |
| Chicago, IL               | Chicago                   | 41.8755616   | -87.6244212  |
| 10001                     | New York                  | 40.7484      | -73.9967     |
| Los Angeles, ca           | Los Angeles               | 34.0536909   | -118.242766  |
| 00501                     | Suffolk County            | 40.8154      | -73.0451     |
| san juan, pr              | San Juan                  | 18.465299    | -66.116666   |
| 00901                     | Río Piedras               | 18.4663      | -66.1057     |
| 96913                     | Mangilau Municipality     | 13.4443      | 144.7863     |
| Hagatna, GU               | Hagåtña                   | 13.4748148   | 144.7516191  |
| New York, NY              | New York                  | 40.7127281   | -74.0060152  |
|-------------------------------------------------------------------------------------|
{SKIPPED_MESSAGE}
"""
