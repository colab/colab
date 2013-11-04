from haystack.utils import Highlighter
from django.conf import settings
from django.utils.html import escape, strip_tags


class ColabHighlighter(Highlighter):
    def highlight(self, text_block):
        self.text_block = escape(strip_tags(text_block))
        highlight_locations = self.find_highlightable_words()
        start_offset, end_offset = self.find_window(highlight_locations)
        return self.render_html(highlight_locations, start_offset, end_offset)

    def find_window(self, highlight_locations):
        """Getting the HIGHLIGHT_NUM_CHARS_BEFORE_MATCH setting
        to find how many characters before the first word found should
        be removed from the window
        """

        if len(self.text_block) <= self.max_length:
            return (0, self.max_length)

        num_chars_before = getattr(
            settings,
            'HIGHLIGHT_NUM_CHARS_BEFORE_MATCH',
            0
        )

        best_start, best_end = super(ColabHighlighter, self).find_window(
            highlight_locations
        )
        if best_start <= num_chars_before:
            best_end -= best_start
            best_start = 0
        else:
            best_start -= num_chars_before
            best_end -= num_chars_before

        return (best_start, best_end)
