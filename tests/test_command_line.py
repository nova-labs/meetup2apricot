"""Test the command line options."""

import meetup2apricot.command_line as command_line


def parse_without_args():
    """Parse a command line with no arguments."""
    return command_line.parse_args([])


def parse_command_line(line):
    """Parse the supplied command line."""
    return command_line.parse_args(line.split())


def test_warnings_flag_off():
    """Test the default warnings flag value."""
    args = parse_without_args()
    assert not args.warnings


def test_warnings_flag_short():
    """Test setting the warnings flag with the short argument."""
    args = parse_command_line("-w")
    assert args.warnings


def test_warnings_flag_long():
    """Test setting the warnings flag with the long argument."""
    args = parse_command_line("--warnings")
    assert args.warnings


def test_verbose_flag_off():
    """Test the default verbose flag value."""
    args = parse_without_args()
    assert not args.verbose


def test_verbose_flag_short():
    """Test setting the verbose flag with the short argument."""
    args = parse_command_line("-v")
    assert args.verbose


def test_verbose_flag_long():
    """Test setting the verbose flag with the long argument."""
    args = parse_command_line("--verbose")
    assert args.verbose


def test_logfile_missing():
    """Test the default logfile name."""
    args = parse_without_args()
    assert "meetup2apricot.log" == args.logfile


def test_logfile_short():
    """Test setting the logfile name with the short argument."""
    args = parse_command_line("-l foo.log")
    assert "foo.log" == args.logfile


def test_logfile_long():
    """Test setting the logfile name with the long argument."""
    args = parse_command_line("--logfile foo.log")
    assert "foo.log" == args.logfile


def test_dryrun_flag_short():
    """Test setting the dry run flag with the short argument."""
    args = parse_command_line("-n")
    assert args.dryrun


def test_dryrun_flag_long():
    """Test setting the dry run flag with the long argument."""
    args = parse_command_line("--dryrun")
    assert args.dryrun


def test_dryrun_flag_off():
    """Test the default dry run flag value."""
    args = parse_without_args()
    assert not args.dryrun


def test_report_flag_off():
    """Test the default report flag value."""
    args = parse_without_args()
    assert not args.report


def test_report_flag_short():
    """Test setting the report flag with the short argument."""
    args = parse_command_line("-r")
    assert args.report


def test_report_flag_long():
    """Test setting the report flag with the long argument."""
    args = parse_command_line("--report")
    assert args.report


def test_show_meetup_ids_flag_off():
    """Test the default "show Meetup IDs" flag value."""
    args = parse_without_args()
    assert not args.show_meetup_ids


def test_show_meetup_ids_flag_short():
    """Test setting the "show Meetup IDs" flag with the short argument."""
    args = parse_command_line("-m")
    assert args.show_meetup_ids


def test_show_meetup_ids_flag_long():
    """Test setting the "show Meetup IDs" flag with the long argument."""
    args = parse_command_line("--meetup-ids")
    assert args.show_meetup_ids


def test_skip_missing():
    """Test the default skip list."""
    args = parse_without_args()
    assert args.skip_meetup_ids == []


def test_skip_short():
    """Test setting a skipped Meetup ID with the short argument."""
    args = parse_command_line("-s abcd123")
    assert args.skip_meetup_ids == ["abcd123"]


def test_skip_long():
    """Test setting a skipped Meetup ID with the long argument."""
    args = parse_command_line("--skip abcd123")
    assert args.skip_meetup_ids == ["abcd123"]


def test_skip_multiple():
    """Test setting multiple skipped Meetup IDs."""
    args = parse_command_line("-s abcd123 -s xyz789")
    assert args.skip_meetup_ids == ["abcd123", "xyz789"]


def test_skip_multiple_one_flag():
    """Test setting multiple skipped Meetup IDs with one flag."""
    args = parse_command_line("-s abcd123 xyz789")
    assert args.skip_meetup_ids == ["abcd123", "xyz789"]


def test_skip_multiple_multiple():
    """Test setting multiple skipped Meetup IDs with multiple flags."""
    args = parse_command_line("-s abcd123 efg456 -s xyz789 qrs678")
    assert args.skip_meetup_ids == ["abcd123", "efg456", "xyz789", "qrs678"]


def test_no_meetup_ids():
    """Test a command line with no Meetup IDs."""
    args = parse_without_args()
    assert args.meetup_ids == []


def test_meetup_ids_one():
    """Test a command line with one Meetup ID."""
    args = parse_command_line("abcd")
    assert args.meetup_ids == ["abcd"]


def test_meetup_ids_two():
    """Test a command line with two Meetup IDs."""
    args = parse_command_line("abcd 1234")
    assert args.meetup_ids == ["abcd", "1234"]


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
