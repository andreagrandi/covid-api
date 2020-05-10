import argparse
from covidapi.jh_import import cli as jh_cli
from datetime import date

parser = argparse.ArgumentParser(description="Import data into the database")

subparsers = parser.add_subparsers(
    title="subcommands",
    description="valid subcommands",
    help="use --help after a subcommand for more details",
)

parser_regions = subparsers.add_parser(
    "jh_regions",
    description="Import the John Hopkins CSSE lookup table into the jh_region_info table",
    help="Import John Hopkins CSSE region information",
)

parser_jh_import = subparsers.add_parser(
    "jh",
    description="Import John Hopkins CSSE daily reports into the database",
    help="Import John Hopkins CSSE daily reports",
)

parser_jh_import.add_argument(
    "--from-date",
    metavar="DATE",
    type=date.fromisoformat,
    default=date(year=2020, month=2, day=29),
    help="date to start importing from (default: 2020-02-29)",
)
parser_jh_import.add_argument(
    "--all", help="import all the available data", action="store_true"
)
parser_jh_import.add_argument(
    "--latest", help="import last couple of days of data", action="store_true"
)

parser_regions.set_defaults(func=jh_cli.import_regions)
parser_jh_import.set_defaults(func=jh_cli.import_data)

if __name__ == "__main__":
    args = parser.parse_args()

    try:
        func = args.func
    except AttributeError:
        parser.print_help()
    else:
        func(args)
