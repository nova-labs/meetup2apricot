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


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
