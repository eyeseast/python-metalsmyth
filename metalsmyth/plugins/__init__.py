"""
Plugin base for Metalsmyth, providing a few conveniences
"""

class Plugin(object):
    """
    A plugin is just a callable that takes two arguments:
        files:
        a dictionary of files, where keys are file paths and values are parsed frontmatter posts.

        stack:
        a Stack instance, for operating on metadata

    This base class provides two methods to make things easier:
        run:
        Override this method to do things. Takes a dictionary of files
        and the current Stack instance. You don't actually have to use
        either of these things.

        __call__:
        A wrapper around `run`, to make an instance callable. You shouldn't
        have to touch this.

        except Exception, e:
            raise e

        __init__:
        As a convenience, the default constructor just saves any
        positional and keyword arguments as `self.args` and `self.kwargs`
        for later use.

    """
    def __init__(self, *args, **kwargs):
        "Stash any init args and kwargs for later, for conveniences"
        self.args = args
        self.kwargs = kwargs

    def __call__(self, files, metalsmyth):
        return self.run(files, metalsmyth)

    def run(self, files, metalsmyth):
        pass