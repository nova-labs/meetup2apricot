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
        other_tags = self.featured_tags(meetup_event)
        code_tags = self.tag_codes(meetup_event.accounting_codes)
        all_tags = other_tags + self.all_event_tags + code_tags
        return list(dict.fromkeys(all_tags))

    def tag_codes(self, codes):
        """Return a list of tags for an event's list of accounting codes."""
        if not codes:
            return []
        code_tags = ["_".join(codes)]
        for code in codes:
            code_tags += self.tag_code(code)
        return code_tags

    def tag_code(self, code):
        """Return a list of tags for an accounting code."""
        return self.codes_to_tags.get(code, [])

    def featured_tags(self, meetup_event):
        """Return a list of codes showing the "featured" status of a Meetup
        event."""
        if meetup_event.featured:
            return ["featured"]
        else:
            return []


def make_event_tagger(codes_to_tags, all_event_tags):
    """Make an event tagger with a mapping of accounting codes to lists of
    tags and a list of tags to apply to all events."""
    cleaned_all_event_tags = clean_tag_list(all_event_tags)
    cleaned_codes_to_tags = clean_codes_to_tags(codes_to_tags)
    return EventTagger(cleaned_codes_to_tags, cleaned_all_event_tags)


def clean_codes_to_tags(raw_codes_to_tags):
    """Given a raw mapping of codes to tags (typically from a configuration
    file), wrap individual string tags in lists."""
    return {code: clean_tag_list(tags) for code, tags in raw_codes_to_tags.items()}


def clean_tag_list(raw_tags_list):
    """Give a list of tags, an individual tag string, or None, return a
    possibly empty list of tags."""
    if not raw_tags_list:
        return []
    if type(raw_tags_list) == str:
        return [raw_tags_list]
    return raw_tags_list


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
