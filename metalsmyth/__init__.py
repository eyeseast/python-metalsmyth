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
        for filename in os.listdir(self.source):
            path = os.path.join(self.source, filename)
            files[filename] = frontmatter.load(path)

        return files

    def run(self, files=None):
        "Run each middleware function on files"
        # use provided files, or load files from source directory
        if files is None:
            files = self.get_files()

        # loop through each middleware
        for func in self.middleware:

            # call each one, ignoring return value
            func(files, self)

        # store and return the result
        self.files = files
        return files

    def build(self):
        "Build out results to dest directory (creating if needed)"

        # ensure a build dir
        if not os.path.isdir(self.dest):
            os.makedirs(self.dest)

        # make sure we have files
        files = getattr(self, 'files', self.run())

        # write the content of each post to dest, using keys as filenames
        for filename, post in self.files.iteritems():

            # join filename to dest dir
            path = os.path.join(self.dest, filename)
            with open(path, 'w') as f:
                f.write(post.content.encode('utf-8'))




