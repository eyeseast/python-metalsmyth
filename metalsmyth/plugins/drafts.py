"""
This is a simple drafts plugin that filters out any files marked 'draft' in Frontmatter metadata.
"""

def drafts(files, stack):
    "Filter out any files marked 'draft'"
    for path, post in list(files.items()):
        if post.get('draft'):
            del files[path]
