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

from metalsmyth import Stack, PostNotFound

class StackTest(unittest.TestCase):
    "Base class for tests."

    maxDiff = None

    def tearDown(self):
        if self.stack.dest is not None and os.path.exists(self.stack.dest):
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
        self.stack.build('tests/tmp')

        # test that content is copied to dest
        for filename in os.listdir(self.stack.dest):
            # each filename should be a key in files
            post = self.stack.files[filename]
            path = os.path.join(self.stack.dest, filename)
            with codecs.open(path, 'r', 'utf-8') as f:
                content = f.read()

            self.assertEqual(post.content, content)

    def test_simple_middleware(self):
        "Test adding simple middleware using a decorator"
        stack = self.stack

        @stack.use
        def count_files(files, stack):
            stack.metadata['count'] = len(files)

        files = stack.run()

        self.assertEqual(len(files), stack.metadata['count'])
        self.assertTrue(count_files in stack.middleware)


class DraftTest(StackTest):
    """
    Tests involving the drafts plugin
    """
    def setUp(self):
        from metalsmyth.plugins.drafts import drafts
        self.stack = Stack('tests/drafts', drafts)

    def test_drafts(self):
        "Draft posts should be filtered out"
        self.stack.build('tests/tmp')

        self.assertEqual(len(self.stack.files), 1)

        post = list(self.stack.files.values())[0]
        self.assertEqual(post['title'], 'Hello, world!')

    def test_drafts_with_iter(self):
        "Handle stack.iter method with drafts plugin"
        posts = list(self.stack.iter())

        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0]['title'], 'Hello, world!')

    def test_drafts_not_found(self):
        "Ensure a post that isn't there raises NotFound"

        with self.assertRaises(PostNotFound):
            self.stack.get('network-diagrams.markdown')


class DateTest(StackTest):
    """
    Tests involving the dates plugin
    """
    def setUp(self):
        from metalsmyth.plugins.dates import Dates
        self.stack = Stack('tests/dates', Dates('date'))

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
        self.stack = Stack('tests/markup', Markdown(output_format='html5'))

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
        self.stack = Stack('tests/markup')

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

    def setUp(self):
        from metalsmyth.plugins.template import Jinja

        self.jinja = Jinja('tests/templates')
        self.env = Environment(loader=FileSystemLoader('tests/templates'))
        self.stack = Stack('tests/markup', self.jinja)

    def test_templates(self):
        "Render posts with a template"
        raw = self.stack.get_files()
        files = self.stack.run()

        for filename, post in files.items():
            if "template" in post.metadata:
                template = self.env.get_template(post['template'])

                self.assertEqual(post.content, template.render(post=raw[filename]))

    def test_inner_template(self):
        "Ensure post content is rendered as its own template"
        post = frontmatter.load('tests/markup/template.md')
        post.content = self.env.from_string(post.content).render(post.metadata)

        test = self.stack.get('template.md')

        self.assertEqual(test.content, post.content)


class SerializationTest(StackTest):
    """
    Tests of serialization
    """
    def setUp(self):
        "Use a stack with lots of things"
        from metalsmyth.plugins.markup import Markdown, Bleach
        self.stack = Stack('tests/markup', Bleach(strip=True), Markdown())

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


class SingleTest(StackTest):
    """
    Tests for getting single files
    """
    def setUp(self):
        from metalsmyth.plugins.markup import Markdown, Bleach
        self.stack = Stack('tests/markup', Bleach(strip=True), Markdown())

    def test_get_file(self):
        "Test getting a single processed file"
        post = frontmatter.load('tests/markup/ebola.md',
            filename='ebola.md', slug='ebola')
        post.content = bleach.clean(post.content, strip=True)
        post.content = markdown(post.content)

        test = self.stack.get('ebola.md')

        self.assertEqual(post.metadata, test.metadata)
        self.assertEqual(post.content, test.content)

    def test_get_cached_file(self):
        "Make sure file is cached"
        raw = frontmatter.load('tests/markup/ebola.md')
        post1 = self.stack.get('ebola.md')

        # change middleware so output is different
        self.stack.middleware = []

        # this shouldn't change
        post2 = self.stack.get('ebola.md')

        # resetting should reprocess
        post3 = self.stack.get('ebola.md', reset=True)

        # posts 1 and 2 should be the same
        self.assertEqual(post1.to_dict(), post2.to_dict())

        # post 3 should be a noop, like raw
        self.assertEqual(post3.content, raw.content)


class IterTest(StackTest):
    """
    Test iterator method
    """
    def setUp(self):
        from metalsmyth.plugins.markup import Markdown, Bleach
        self.stack = Stack('tests/markup', Bleach(strip=True), Markdown())

    def test_iterator(self):
        "Test Stack.iter"
        posts = self.stack.run()
        posts = sorted(posts.values(), key=lambda p: p['filename'])

        tests = self.stack.iter(reset=True)

        for test, post in zip(tests, posts):
            self.assertEqual(test.to_dict(), post.to_dict())

    def test_iterator_reversed(self):
        "Stack.iter in reverse order"
        posts = self.stack.run()
        posts = sorted(posts.values(), key=lambda p: p['filename'], reverse=True)

        tests = self.stack.iter(reset=True, reverse=True)

        for test, post in zip(tests, posts):
            self.assertEqual(test.to_dict(), post.to_dict())


if __name__ == "__main__":
    unittest.main()