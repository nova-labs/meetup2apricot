import time
from collections import deque


class Throttle:

    """Throttles activity at some rate per some time span."""

    def __init__(self, rate, time_span):
        """Initialize with a rate (integer number of events) and a time span
        (seconds)."""
        self.time_span = time_span
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


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
