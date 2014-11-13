"""
Convert content to html with markdown (and possibly other formats)
"""
import markdown

from . import Plugin


class Markdown(Plugin):
    """
    Convert markdown content to HTML. Options set in __init__ will be passed to parser.
    """
    def __init__(self, **options):
        self.md = markdown.Markdown(**options)

    def run(self, files, metalsmyth):
        "Convert files"
        for filename, post in files.iteritems():
            # reset first to clear any extension state
            post.content = self.md.reset().convert(post.content)
