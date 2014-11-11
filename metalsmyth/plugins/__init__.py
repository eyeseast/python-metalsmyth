"""
Plugin base for Metalsmyth, providing a few conveniences
"""

class Plugin(object):
    """
    A plugin is just a callable that takes two arguments:
        files:
        a dictionary of files, where keys are file paths and values are parsed frontmatter posts.

        metalsmyth:
        a metalsmyth instance, for operating on metadata

    This base class provides two methods to make things easier:
        run:
        override this method to do things

        __call__:
        a wrapper around `run`, to make an instance callable

    """

    def __call__(self, files, metalsmyth):
        return self.run(files, metalsmyth)

    def run(self, files, metalsmyth):
        pass