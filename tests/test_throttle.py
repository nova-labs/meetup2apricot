""" Test throttles."""

from meetup2apricot.throttle import Throttle, make_throttle
import time
import logging
import pytest


def test_is_ready_init():
    """Test that a throttle is ready after initialization."""
    throttle = Throttle(1, 60)
    assert throttle.is_ready()


def test_is_ready_ok():
    """Test that a throttle is ready after its time span."""
    throttle = Throttle(1, 60)
    throttle.event(1000)
    assert throttle.is_ready(1060)


def test_is_ready_not():
    """Test that a throttle is not ready before its time span."""
    throttle = Throttle(1, 60)
    throttle.event(1000)
    assert not throttle.is_ready(1059)


def test_throttle_ready_now():
    """Test throttling when no delay is needed."""
    throttle = Throttle(1, 60)
    throttle.event(1000)
    start_time = time.time()
    throttle.throttle(1060)
    end_time = time.time()
    assert start_time == pytest.approx(end_time, abs=1e-2)


def test_throttle_ready_soon():
    """Test throttling when some delay is needed."""
    throttle = Throttle(1, 60)
    throttle.event(1000)
    start_time = time.time()
    throttle.throttle(1059.9)
    end_time = time.time()
    assert start_time + 0.1 == pytest.approx(end_time, abs=1e-2)


def test_make_throttle_ok(caplog):
    """Test making a throttle when the utilization factor is within limits."""
    throttle = make_throttle(
        rate=40, time_span=63, utilization_factor=0.75, purpose="test 1"
    )
    assert caplog.messages == []
    assert type(throttle) == Throttle
    assert throttle.rate == 30
    assert throttle.time_span == 63


def test_make_throttle_debug(caplog):
    """Test making a throttle with debug logging."""
    caplog.set_level(logging.DEBUG)
    make_throttle(rate=40, time_span=63, utilization_factor=0.75, purpose="test 1")
    assert caplog.messages == ["purpose='test 1' rate=30 time_span=63"]


def test_make_throttle_low(caplog):
    """Test making a throttle when the utilization factor is below limits."""
    expected_message = (
        "utilization_factor must be between 0.05 and 0.95. "
        "purpose='test 2' rate=400 time_span=63 utilization_factor=0.000000"
    )
    throttle = make_throttle(
        rate=400, time_span=63, utilization_factor=0, purpose="test 2"
    )
    assert caplog.messages == [expected_message]
    assert type(throttle) == Throttle
    assert throttle.rate == 20
    assert throttle.time_span == 63


def test_make_throttle_high(caplog):
    """Test making a throttle when the utilization factor is above limits."""
    expected_message = (
        "utilization_factor must be between 0.05 and 0.95. "
        "purpose='test 3' rate=400 time_span=63 utilization_factor=1.000000"
    )
    throttle = make_throttle(
        rate=400, time_span=63, utilization_factor=1, purpose="test 3"
    )
    assert caplog.messages == [expected_message]
    assert type(throttle) == Throttle
    assert throttle.rate == 380
    assert throttle.time_span == 63


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
