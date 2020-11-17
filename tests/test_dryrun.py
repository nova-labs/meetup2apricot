"""Test the dry run decorator."""


from meetup2apricot.dryrun import dryrunnable, method, log_method_call
from .pytest_regex import PytestRegex
import logging
import pytest


class Sample:

    """A sample class for testing the dry run decorator."""

    def __init__(self, dryrun=False, other_flag=False):
        """Initialize with a dryrun flag."""
        self.dryrun = dryrun
        self.other_flag = other_flag
        self.calls = []

    @method()
    def no_args(self):
        """A method with no args."""
        message = "no_args"
        self.calls.append(message)
        return message

    @method()
    def some_args(self, x, y, z=3):
        """A method with some args."""
        message = f"some args x={x} y={y} z={z}"
        self.calls.append(message)
        return message

    @method("other_flag")
    def other_flag_no_args(self):
        """A method with no args controlled by the other flag."""
        message = "other_flag_no_args"
        self.calls.append(message)
        return message

@dryrunnable()
class DecoratedSample:

    """A sample decorated class for testing the dry run decorator."""

    def __init__(self, a, b):
        """Initialize with some data."""
        self.a = a
        self.b = b


@pytest.fixture
def production_sample(caplog):
    """Return a sample ready to run."""
    caplog.set_level(logging.INFO)
    return Sample()


@pytest.fixture
def dryrun_sample(caplog):
    """Return a sample that will dry run decorated methods."""
    caplog.set_level(logging.INFO)
    return Sample(dryrun=True)


@pytest.fixture
def other_flag_sample(caplog):
    """Return a sample that will dry run "other flag" methods."""
    caplog.set_level(logging.INFO)
    return Sample(other_flag=True)


def test_production_no_args(production_sample, caplog):
    """Test a production run of the no_args method."""
    assert production_sample.no_args() == "no_args"
    assert production_sample.calls == ["no_args"]
    assert caplog.messages == []


def test_production_some_args(production_sample, caplog):
    """Test a production run of the some_args method."""
    assert production_sample.some_args(1, y=2) == "some args x=1 y=2 z=3"
    assert production_sample.calls == ["some args x=1 y=2 z=3"]
    assert caplog.messages == []


def test_production_other_flag_no_args(production_sample, caplog):
    """Test a production run of the other_flag_no_args method."""
    assert production_sample.other_flag_no_args() == "other_flag_no_args"
    assert production_sample.calls == ["other_flag_no_args"]
    assert caplog.messages == []


def test_dryrun_no_args(dryrun_sample, caplog):
    """Test a dryrun run of the no_args method."""
    assert dryrun_sample.no_args() is None
    assert dryrun_sample.calls == []
    assert caplog.messages == [
        PytestRegex(
            r"Skipped <tests.test_dryrun.Sample object at 0x[0-9a-f]+>.no_args\(\)"
        )
    ]


def test_dryrun_some_args(dryrun_sample, caplog):
    """Test a dryrun run of the some_args method."""
    assert dryrun_sample.some_args(1, y=2) is None
    assert dryrun_sample.calls == []
    assert caplog.messages == [
        PytestRegex(
            r"Skipped <tests.test_dryrun.Sample object at 0x[0-9a-f]+>.some_args\(1, y=2\)"
        )
    ]


def test_dryrun_other_flag_no_args(dryrun_sample, caplog):
    """Test a dryrun run of the other_flag_no_args method."""
    assert dryrun_sample.other_flag_no_args() == "other_flag_no_args"
    assert dryrun_sample.calls == ["other_flag_no_args"]
    assert caplog.messages == []


def test_other_flag_no_args(other_flag_sample, caplog):
    """Test a other_flag run of the no_args method."""
    assert other_flag_sample.no_args() == "no_args"
    assert other_flag_sample.calls == ["no_args"]
    assert caplog.messages == []


def test_other_flag_some_args(other_flag_sample, caplog):
    """Test a other_flag run of the some_args method."""
    assert other_flag_sample.some_args(1, y=2) == "some args x=1 y=2 z=3"
    assert other_flag_sample.calls == ["some args x=1 y=2 z=3"]
    assert caplog.messages == []


def test_other_flag_other_flag_no_args(other_flag_sample, caplog):
    """Test a other_flag run of the other_flag_no_args method."""
    assert other_flag_sample.other_flag_no_args() is None
    assert other_flag_sample.calls == []
    assert caplog.messages == [
        PytestRegex(
            r"Skipped <tests.test_dryrun.Sample object at 0x[0-9a-f]+>.other_flag_no_args\(\)"
        )
    ]

def test_decorated_sample_implicit():
    """Test initializing the decorated sample class without setting the dry run
    flag."""
    sample = DecoratedSample(4, b=5)
    assert sample.a == 4
    assert sample.b == 5
    assert sample.dryrun == False

def test_decorated_sample_explicit():
    """Test initializing the decorated sample class, setting the dry run
    flag."""
    sample = DecoratedSample(4, dryrun=True, b=5)
    assert sample.a == 4
    assert sample.b == 5
    assert sample.dryrun == True

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
