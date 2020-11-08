"""Tag events based on Meetup event title accounting codes. Wild Apricot can
filter events by tag to show, for example, a list of woodworking events."""

class EventTagger:

    """Tags events based on accounting codes that prefix event titles."""

    def __init__(self, codes_to_tags, all_event_tags):
        """Initialize with a mapping of accounting codes to lists of tags and a
        list of tags to apply to all events."""
        self.codes_to_tags = codes_to_tags
        self.all_event_tags = all_event_tags

    def tag_event(self, meetup_event):
        """Return a list of tags for a Meetup event."""
        return self.tag_code(meetup_event.accounting_code)

    def tag_code(self, code):
        """Return a list of tags for an accounting code."""
        if code is None:
            return self.all_event_tags
        code_tags = self.codes_to_tags.get(code, [])
        return code_tags + self.all_event_tags


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
