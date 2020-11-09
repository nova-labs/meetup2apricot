""" Test throttles."""

from meetup2apricot.throttle import Throttle
import time
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
    assert start_time + .1 == pytest.approx(end_time, abs=1e-2)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
