# Metalsmyth

[![Build Status](https://travis-ci.org/eyeseast/python-metalsmyth.svg)](https://travis-ci.org/eyeseast/python-metalsmyth)

This is a little library to process a directory of files with a stack of middleware. It is based on [metalsmith](http://www.metalsmith.io/), which is built in and for Node. This version uses the same three-step process:

1. Read all the files in a source directory.
2. Invoke a series of plugins that manipulate the files.
3. Write the results to a destination directory!

Each plugin is simply a callable that takes a dictionary of files, plus a `Stack` instance, and does something. It doesn't actually have to operate on (or return) the files. Each file is parsed for YAML Frontmatter, with file paths as keys (relative to the source directory).

A few plugins are included by default:

 - drafts: filter out posts where `draft` is `true`
 - dates: convert a date field to a Python `datetime.datetime` object
 - markdown: convert post content to HTML using markdown
 - bleach: run `bleach.clean` on post content
 - linkify: run `bleach.linkify` on post content


## Usage

```python
from metalsmyth import Stack
from metalsmyth.plugins.dates import Dates
from metalsmyth.plugins.markup import Bleach, Markdown

# create a stack with a source directory, destination and middleware
stack = Stack('tests/markup', 'tests/tmp',
    Dates('date'), 
    Bleach(strip=True), 
    Markdown(output_format='html5')
)

# get processed files
files = stack.run()

# or build to stack.dest
stack.build()
```