from haystack.utils import Highlighter
 
 
class ColabHighlighter(Highlighter):
    def find_window(self, highlight_locations):
        return (0, self.max_length)
