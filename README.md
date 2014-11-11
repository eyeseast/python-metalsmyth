# What do I call this thing?

This is a little library to process a directory of files with a stack of middleware. It is based on [metalsmith](http://www.metalsmith.io/), which is built in and for Node. This version uses the same three-step process:

1. Read all the files in a source directory.
2. Invoke a series of plugins that manipulate the files.
3. Write the results to a destination directory!

Each plugin is simply a callable that takes a dictionary of files, plus a `Stack` instance, and does something. It doesn't actually have to operate on (or return) the files. Each file is parsed for YAML Frontmatter, with file paths as keys (relative to the source directory).