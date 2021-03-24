"""Command line options."""

import argparse

parser = argparse.ArgumentParser(description="Download Meetup events into Wild Apricot")

parser.add_argument(
    "-d",
    "--debug",
    action="store_true",
    help="Log debug messages (default: info and higher)",
)

parser.add_argument(
    "-l",
    "--logfile",
    default="meetup2apricot.log",
    help="Path to logfile (default: %(default)s)",
)

parser.add_argument(
    "-m",
    "--meetup-ids",
    dest="show_meetup_ids",
    action="store_true",
    help="Show Meetup event IDs in reports.",
)

parser.add_argument(
    "-n",
    "--dryrun",
    action="store_true",
    help="Do not add events to Wild Apricot, download photos, or update cached data",
)

parser.add_argument(
    "-r",
    "--report",
    action="store_true",
    help="Report added events, photos, and registration types to standard output",
)

parser.add_argument(
    "-s",
    "--skip",
    action="append",
    default=[],
    metavar="MEETUP_ID",
    help="Skip the Meetup ID",
)

parser.add_argument(
    "-v", "--verbose", action="store_true", help="Log to standard error"
)

parser.add_argument(
    "-w", "--warnings", action="store_true", help="Log warnings to standard error"
)

parser.add_argument(
    "meetup_ids",
    nargs="*",
    metavar="MEETUP_ID",
    help="Meetup ID of an event to download",
)


def parse_args(args=None):
    return parser.parse_args(args)


if __name__ == "__main__":

    parse_args(["--help"])

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
