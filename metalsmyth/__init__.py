"""
The core of Metalsmyth (this really needs a better name) is a Stack,
which reads files from a source directory, registers middleware
and processes files.
"""
import glob
import os

import frontmatter


class Stack(object):
    """
    A Stack takes a source directory, output directory, optional middleware and metadata
    """
    def __init__(self, source='src', dest='build', *middleware, **metadata):
        self.source = source
        self.dest = dest
        self.middleware = list(middleware)
        self.metadata = dict(metadata)

    def get_files(self):
        """
        Read and parse files from a directory,
        return a dictionary of path => post
        """
        files = {}
        for filename in os.listdir(self.src):
            path = os.path.join(self.src, filename)
            files[filename] = frontmatter.load(path)

        return files

    def run(self):
        "Run each middleware function on files"
        # load files from source directory
        files = self.get_files()

        # loop through each middleware
        for func in self.middleware:

            # call each one, ignoring return value
            func(files, self)

        # store and return the result
        self.files = files
        return files

    


