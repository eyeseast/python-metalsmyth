#!/usr/bin/env python
import codecs
import datetime
import os
import shutil
import unittest

import bleach
import frontmatter
from jinja2 import Environment, FileSystemLoader
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
            set(os.listdir(self.stack.source)),
            set(os.listdir(self.stack.dest))
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

        post = list(self.stack.files.values())[0]
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
        self.stack = Stack('tests/markup', 'tests/tmp', Markdown(output_format='html5'))

    def test_markown(self):
        "Post.content should be converted to HTML"
        raw = self.stack.get_files()
        files = self.stack.run()

        for filename, post in files.items():
            self.assertEqual(
                post.content,
                markdown(raw[filename].content, output_format='html5')
            )


class BleachTest(StackTest):
    """
    Tests for bleach-related plugins
    """
    def setUp(self):
        # add middleware on each test
        self.stack = Stack('tests/markup', 'tests/tmp')

    def test_clean(self):
        from metalsmyth.plugins.markup import Bleach
        self.stack.middleware.append(Bleach(tags=[], strip=True))

        raw = self.stack.get_files()
        files = self.stack.run()

        for filename, post in files.items():
            cleaned = bleach.clean(raw[filename].content, tags=[], strip=True)
            self.assertEqual(post.content, cleaned)

    def test_linkify(self):
        from metalsmyth.plugins.markup import Linkify
        self.stack.middleware.append(Linkify())

        raw = self.stack.get_files()
        files = self.stack.run()

        for filename, post in files.items():
            linked = bleach.linkify(raw[filename].content)
            self.assertEqual(post.content, linked)


class TemplateTest(StackTest):
    """
    Tests for the template plugin
    """
    maxDiff = None

    def setUp(self):
        from metalsmyth.plugins.template import Jinja

        self.jinja = Jinja('tests/templates')
        self.env = Environment(loader=FileSystemLoader('tests/templates'))
        self.stack = Stack('tests/markup', 'tests/tmp', self.jinja)

    def test_templates(self):
        "Render posts with a template"
        raw = self.stack.get_files()
        files = self.stack.run()

        for filename, post in files.items():
            template = self.env.get_template(post['template'])

            self.assertEqual(post.content, template.render(post=raw[filename]))


class SerializationTest(StackTest):
    """
    Tests of serialization
    """
    def setUp(self):
        "Use a stack with lots of things"
        from metalsmyth.plugins.markup import Markdown, Bleach

        self.stack = Stack('tests/markup', 'tests/tmp', Bleach(strip=True), Markdown())

    def test_dict_export(self):
        files = self.stack.run()
        data = self.stack.serialize(as_dict=True)

        for filename, post in data.items():
            self.assertEqual(post, files[filename].to_dict())

    def test_list_export(self):
        files = self.stack.run()
        posts = sorted(files.values(), key=lambda p: p['title'])
        data = self.stack.serialize(sort=lambda p: p['title'])

        for p1, p2 in zip(posts, data):
            self.assertEqual(p1.to_dict(), p2)


if __name__ == "__main__":
    unittest.main()