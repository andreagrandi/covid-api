import argparse
from covidapi import import_data_jh
from datetime import date

parser = argparse.ArgumentParser(description='Import data into the database')

subparsers = parser.add_subparsers(
    title='subcommands',
    description='valid subcommands',
    help='use --help after a subcommand for more details'
)

parser_jh_import = subparsers.add_parser('jh', description='Import John Hopkins CSSE data into the database', help='Import John Hopkins CSSE data')

parser_jh_import.add_argument(
    '--from-date',
    metavar='DATE',
    type=date.fromisoformat,
    default=date(year=2020, month=2, day=29),
    help='date to start importing from (default: 2020-02-29)'
)
parser_jh_import.add_argument("--all", help="import all the available data", action="store_true")
parser_jh_import.add_argument("--latest", help="import last couple of days of data", action="store_true")

parser_jh_import.set_defaults(func=import_data_jh.main)

if __name__ == '__main__':
    args = parser.parse_args()

    try:
        args.func(args)
    except AttributeError:
        parser.print_help()
