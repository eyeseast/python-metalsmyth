#!/usr/bin/env python
import codecs
import datetime
import os
import shutil
import unittest
import frontmatter
from markdown import markdown

from metalsmyth import Stack

class StackTest(unittest.TestCase):
    "Base class for tests."

    def tearDown(self):
        if os.path.exists(self.stack.dest):
            shutil.rmtree(self.stack.dest)


class NoopTest(StackTest):
    """
    Tests involving the noop example
    """
    def setUp(self):
        self.stack = Stack('tests/noop', dest='tests/tmp')

    def test_build(self):
        "Test that file contents are copied to dest"
        self.stack.build()

        # same filenames should be present
        self.assertEqual(
            os.listdir(self.stack.source),
            os.listdir(self.stack.dest)
        )

    def test_built_content(self):
        "Test that content is copied"
        self.stack.build()

        # test that content is copied to dest
        for filename in os.listdir(self.stack.dest):
            # each filename should be a key in files
            post = self.stack.files[filename]
            path = os.path.join(self.stack.dest, filename)
            with codecs.open(path, 'r', 'utf-8') as f:
                content = f.read()

            self.assertEqual(post.content, content)


class DraftTest(StackTest):
    """
    Tests involving the drafts plugin
    """
    def setUp(self):
        from metalsmyth.plugins.drafts import drafts
        self.stack = Stack('tests/drafts', 'tests/tmp', drafts)

    def test_drafts(self):
        "Draft posts should be filtered out"
        self.stack.build()

        self.assertEqual(len(self.stack.files), 1)

        post = self.stack.files.values()[0]
        self.assertEqual(post['title'], 'Hello, world!')


class DateTest(StackTest):
    """
    Tests involving the dates plugin
    """
    def setUp(self):
        from metalsmyth.plugins.dates import Dates
        self.stack = Stack('tests/dates', 'tests/tmp', Dates('date'))

    def test_dates(self):
        "Dates should get parsed to datetimes"
        files = self.stack.run()

        for post in files.values():
            self.assertTrue(isinstance(post['date'], datetime.datetime))

        self.assertEqual(
            files['hello.markdown']['date'],
            datetime.datetime(2013, 6, 7)
        )

        self.assertEqual(
            files['network-diagrams.markdown']['date'],
            datetime.datetime(2014, 3, 4)
        )


class MarkdownTest(StackTest):
    """
    Tests for the markdown plugin
    """
    def setUp(self):
        from metalsmyth.plugins.markup import Markdown
        self.stack = Stack('tests/dates', 'tests/tmp', Markdown())

    def test_markown(self):
        "Post.content should be converted to HTML"
        raw = self.stack.get_files()
        files = self.stack.run()

        for filename, post in files.iteritems():
            self.assertEqual(
                post.content,
                markdown(raw[filename].content)
            )


class BleachTest(StackTest):
    """
    Tests for bleach-related plugins
    """
    def setUp(self):
        # add middleware on each test
        self.stack = Stack('tests/dates', 'tests/tmp')

    def test_clean(self):
        pass

    def test_linkify(self):
        pass


if __name__ == "__main__":
    unittest.main()