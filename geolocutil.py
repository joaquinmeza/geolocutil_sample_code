import argparse
import json
import sys
from argparse import RawTextHelpFormatter
from src.GeoLocationData import GeoLocationData, GeoResult


WIDTH = 89
SEPARATOR = '-'

class GeoResultEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, GeoResult):
            return {
                "search_term": obj.search_term,
                "name": obj.name,
                "lat": obj.lat,
                "lon": obj.lon
            }
        return super().default(obj)


def table_print(locations):

    def line_separator():
        print(f"|{SEPARATOR * (WIDTH - 4)}|")

    def to_print(_search_term, _name, _lat, _lon):
        msg = f"| {_search_term:<25} | {_name:<25} | {_lat:<12} | {_lon:<12} |"
        print(msg)

    def header():
        line_separator()
        to_print('Search Term', 'City/Town Name', 'Latitude', 'Longitude')
        line_separator()

    header()

    for location in locations:
        search_term = location['search_term'][:25]
        name = location['name'][:25]
        lat = str(location['lat'])[:12]
        lon = str(location['lon'])[:12]
        to_print(search_term, name, lat, lon)
    line_separator()

def main() -> None:
    __help_message = (
        "A list of locations (\"City, ST\" or zip code in 5 digit format \"12345\") - US Cities and Zip codes only.\nExamples:\n\t'Madison, WI'\n\t'12345'\n\t"
        "'Madison, WI' '12345' 'Chicago, IL' '10001'"
    )

    parser = argparse.ArgumentParser(
        description="Retrieves geolocation data utilizing Open Weather Geocoding API",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument("-p", "--print", action="store_true", help="Outputs pretty print to stdout instead of json string")
    parser.add_argument("-j", "--json", action="store_true", help="Converts all strings to ascii in json output")
    parser.add_argument("-e", "--errors", action="store_true", help="Prints out Error messages to stdout")

    parser.add_argument(
        "locations",
        nargs="+",
        help=__help_message,
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    geolocation = GeoLocationData()
    geolocs = geolocation(args.locations)

    if args.print is True:
        table_print(geolocs)
    else:
        print(json.dumps(geolocs, cls=GeoResultEncoder, indent=4, ensure_ascii=args.json))

    if args.errors:
        for error in geolocation.errors:
            print(error)
    else:
        print("Any queries not included was skipped due to an error.  Please use `-e` in the function call to include errors in the output.")


if __name__ == "__main__":
    main()