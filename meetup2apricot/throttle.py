"""Activity throttles typically used to keep API call rates below allowed
limits."""

import logging
import time
from collections import deque

MIN_UTILIZATION = 0.05
MAX_UTILIZATION = 0.95


class Throttle:

    """Throttles activity at some rate per some time span."""

    def __init__(self, rate, time_span):
        """Initialize with a rate (integer number of events) and a time span
        (seconds)."""
        self.time_span = time_span
        self.rate = rate
        self.ready_times = deque([0] * rate, rate)

    def is_ready(self, current_time=None):
        """Check whether the throttle is ready for another event at the current
        time."""
        now = current_time or time.time()
        return now >= self.ready_times[0]

    def event(self, current_time=None):
        """Record an event at the current time."""
        now = current_time or time.time()
        self.ready_times.append(now + self.time_span)

    def wait(self, current_time=None):
        """Wait until the next ready time."""
        now = current_time or time.time()
        while not self.is_ready(now):
            sleep_time = self.ready_times[0] - now
            time.sleep(sleep_time)
            now = time.time()

    def throttle(self, current_time=None):
        """Throttle an event, waiting until the next ready time."""
        self.wait(current_time)
        self.event()


def make_throttle(rate, time_span, utilization_factor, purpose):
    """Return a new throttle given a rate (integer number of events), a time
    span (seconds), a utilization factor (number between 0.05 and 0.95), and a
    purpose (for logging)."""
    logger = logging.getLogger("make_throttle")
    if not (MIN_UTILIZATION <= utilization_factor <= MAX_UTILIZATION):
        logger.warning(
            "utilization_factor must be between %0.2f and %0.2f. "
            "purpose=%r rate=%d time_span=%d utilization_factor=%f",
            MIN_UTILIZATION,
            MAX_UTILIZATION,
            purpose,
            rate,
            time_span,
            utilization_factor,
        )
        utilization_factor = max(
            MIN_UTILIZATION, min(MAX_UTILIZATION, utilization_factor)
        )
    allocated_rate = round(rate * utilization_factor)
    logger.debug("purpose=%r rate=%d time_span=%d", purpose, allocated_rate, time_span)
    return Throttle(allocated_rate, time_span)


class OpenThrottle:

    """Allows work to proceed at full speed: an open throttle."""

    def throttle(self, current_time=None):
        """Pretend to throttle an event. Proceed without slowing."""
        pass


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
