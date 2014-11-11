"""
This is a simple drafts plugin that filters out any files marked 'draft' in Frontmatter metadata.
"""

def drafts(files, metalsmyth):
    "Filter out any files marked 'draft'"
    for path, post in files.iteritems():
        if post.get('draft'):
            del files[path]
