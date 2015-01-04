"""
The core of Metalsmyth (this really needs a better name) is a Stack,
which reads files from a source directory, registers middleware
and processes files.
"""
import glob
import os

import frontmatter


class PostNotFound(Exception):
    """
    Error when a post isn't where you think it is
    """


class Stack(object):
    """
    A Stack takes a source directory, output directory, optional middleware and metadata
    """
    def __init__(self, source='src', *middleware, **metadata):
        self.source = source
        self.dest = metadata.pop('dest', None)
        self.middleware = list(middleware)
        self.metadata = dict(metadata)
        self.files = {}

    def get_files(self):
        """
        Read and parse files from a directory,
        return a dictionary of path => post
        """
        files = {}
        for filename in os.listdir(self.source):
            path = os.path.join(self.source, filename)
            files[filename] = frontmatter.load(path, 
                filename=filename, 
                slug=os.path.splitext(filename)[0])

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
        self.files.update(files)
        return files

    def iter(self, reset=False, reverse=False):
        """
        Yield processed files one at a time, in natural order.
        """
        files = os.listdir(self.source)
        files.sort(reverse=reverse)

        for filename in files:
            try:
                yield self.get(filename, reset)
            except PostNotFound:
                continue

    def get(self, filename, reset=False):
        """
        Get a single processed file. Uses a cached version
        if `run` has already been called, unless `reset` is True.
        """
        if filename in self.files and not reset:
            return self.files[filename]

        # load a single file, and process
        files = {}
        path = os.path.join(self.source, filename)
        files[filename] = frontmatter.load(path, 
            filename=filename,
            slug=os.path.splitext(filename)[0])

        # call middleware
        for func in self.middleware:
            func(files, self)

        # cache the processed post
        self.files.update(files)

        # return just the post
        try:
            return files[filename]
        except KeyError:
            raise PostNotFound('{0} not found'.format(filename))

    def build(self, dest=None):
        "Build out results to dest directory (creating if needed)"
        # dest can be set here or on init
        if not dest:
            dest = self.dest

        # raise an error if dest is None
        if dest is None:
            raise ValueError('destination directory must not be None')

        # store build dir for later
        self.dest = dest

        # ensure a build dir
        if not os.path.isdir(self.dest):
            os.makedirs(self.dest)

        # make sure we have files
        if not self.files:
            self.run()

        # write the content of each post to dest, using keys as filenames
        for filename, post in self.files.items():

            # join filename to dest dir
            path = os.path.join(self.dest, filename)
            with open(path, 'wb') as f:
                f.write(post.content.encode('utf-8'))

    def serialize(self, as_dict=False, sort=None):
        """
        Dump built files as a list or dictionary, for JSON or other serialization.

            sort: a key function to sort a list, or simply True
        """
        files = getattr(self, 'files', self.run())

        if as_dict:
            return dict((fn, p.to_dict()) for fn, p in files.items())

        # generate a list
        data = (p.to_dict() for p in files.values())

        if callable(sort):
            return sorted(data, key=sort)

        elif sort is True:
            return sorted(data)

        return list(data)

    def use(self, func):
        """
        Add function (or other callable) to the middleware stack.
        Takes a single function as an argument and returns it,
        so this can be used as a decorator.

        func should take two arguments: files and stack

        @stack.use
        def count_files(files, stack):
            stack.metadata['count'] = len(files)

        """
        if not callable(func):
            raise TypeError('Stack.use requires a callable')

        self.middleware.append(func)
        return func

