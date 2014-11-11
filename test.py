#!/usr/bin/env python
import codecs
import os
import shutil
import unittest
import frontmatter

from metalsmyth import Stack

class NoopTest(unittest.TestCase):
    """
    Tests involving the noop example
    """
    def setUp(self):
        self.stack = Stack('tests/noop', dest='tests/tmp')

    def tearDown(self):
        shutil.rmtree(self.stack.dest)

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


if __name__ == "__main__":
    unittest.main()