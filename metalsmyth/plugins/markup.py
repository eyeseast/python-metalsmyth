"""
Convert content to html with markdown (and possibly other formats)
"""
from . import Plugin


class Markdown(Plugin):
    """
    Convert markdown content to HTML. Options set in __init__ will be passed to parser.
    """
    def __init__(self, **options):
        # import and initialize here
        import markdown
        self.md = markdown.Markdown(**options)

    def run(self, files, stack):
        "Convert files"
        for filename, post in files.items():
            # reset first to clear any extension state
            post.content = self.md.reset().convert(post.content)


class Bleach(Plugin):
    """
    Clean HTML. Options kwargs set in __init__ will be used with bleach.clean
    """
    def __init__(self, *args, **kwargs):
        # import and stash here to minimize dependencies
        import bleach

        self.bleach = bleach
        self.args = list(args)
        self.kwargs = dict(kwargs)

    def run(self, files, stack):
        "Clean your text"
        for filename, post in files.items():
            post.content = self.bleach.clean(post.content, *self.args, **self.kwargs)


class Linkify(Plugin):
    """
    Run bleach.linkify on post.content
    """
    def __init__(self, *args, **kwargs):
        # again, import here
        import bleach

        self.bleach = bleach
        self.args = list(args)
        self.kwargs = dict(kwargs)
    
    def run(self, files, stack):
        "Linkify your text"
        for filename, post in files.items():
            post.content = self.bleach.linkify(post.content, *self.args, **self.kwargs)


