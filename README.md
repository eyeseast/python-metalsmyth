# Metalsmyth

[![Build Status](https://travis-ci.org/eyeseast/python-metalsmyth.svg)](https://travis-ci.org/eyeseast/python-metalsmyth)

This is a little library to process a directory of files with a stack of middleware. It is based on [metalsmith](http://www.metalsmith.io/), which is built in and for Node. This version uses the same three-step process:

1. Read all the files in a source directory.
2. Invoke a series of plugins that manipulate the files.
3. Write the results to a destination directory (or do something else!)

Each plugin is simply a callable that takes a dictionary of files, plus a `Stack` instance, and does something. It doesn't actually have to operate on (or return) the files. Each file is parsed for YAML Frontmatter, with file paths as keys (relative to the source directory).

## How is this useful?

I build news applications and interactive stories for a living, often working with other journalists who write text, gather photos and edit video. That content needs to be formatted, cleaned up, organized, combined with other data and whatnot. Then it needs to be put online. 

Metalsmyth is a way of organizing that processing pipeline, from raw text to HTML (or other formats). I'm building it with the intention of using it with [Tarbell](http://tarbell.io) or other static site generators. This can also work as a generator on its own.

A few plugins are included by default:

 - drafts: filter out posts where `draft` is `true`
 - dates: convert a date field to a Python `datetime.datetime` object
 - markdown: convert post content to HTML using markdown
 - bleach: run `bleach.clean` on post content
 - linkify: run `bleach.linkify` on post content

## Install

    $ pip install metalsmyth

By itself, Metalsmyth only needs [Python Frontmatter][fm], which itself relies on [PyYAML][]. If you want to use the bundled plugins, you'll need a few extra libraries:

    $ pip install markdown         # for markdown plugin
    $ pip install bleach           # for bleach and linkify plugins
    $ pip install jinja2           # for jinja template plugin
    $ pip install python-dateutil  # for dates plugin

 [fm]: https://github.com/eyeseast/python-frontmatter
 [PyYAML]: http://pyyaml.org

## Usage

```python
from metalsmyth import Stack
from metalsmyth.plugins.dates import Dates
from metalsmyth.plugins.markup import Bleach, Markdown

# create a stack with a source directory and middleware
stack = Stack('tests/markup', 
    Dates('date'), 
    Bleach(strip=True), 
    Markdown(output_format='html5')
)

# get processed files
files = stack.run()

# or build to a destination directory
stack.build('tests/tmp')
```
