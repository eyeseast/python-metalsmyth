"""
Render posts with templates
"""
import os

from . import Plugin

class Jinja(Plugin):
    """
    Render templates with post as context.
    Use an existing jinja2 environment or simply pass a template directory.
    """
    def __init__(self, template_dir='templates', default_template=None, loader=None, environment=None):
        # do imports here so other template engines can work independently
        from jinja2 import Environment, FileSystemLoader

        # check for environment, then loader, then just build it
        if environment is not None:
            self.env = environment
            self.loader = getattr(environment, 'loader', None)

        elif loader is not None:
            self.env = Environment(loader=loader)
            self.loader = loader

        else:
            self.loader = FileSystemLoader(template_dir)
            self.env = Environment(loader=self.loader)

        if default_template:
            self.default_template = self.env.get_template(default_template)

    def run(self, files, stack):
        "Render templates"
        # make stack available to all templates
        self.env.globals['stack'] = stack

        for filename, post in files.items():
            # render content first
            post.content = self.env.from_string(post.content).render(post.metadata)

            # check for a template field
            if "template" in post.metadata:
                template = self.env.get_template(post['template'])

            # or use the default template
            elif hasattr(self, 'default_template'):
                template = self.default_template

            else: # no template, so bail
                continue

            # at this point, we have a template, so render
            post.content = template.render(post=post)
