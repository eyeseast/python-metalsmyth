"""
Plugin to parse dates into a proper Python datetime
"""
from dateutil.parser import parse

from . import Plugin


class Dates(Plugin):
    """
    Given a date field name, turn that field into a proper datetime
    """
    
    def __init__(self, date_field='date'):
        self.date_field = date_field
    
    def run(self, files, stack):
        "Convert dates"
        for filename, post in files.items():
            if self.date_field in post.metadata:
                post[self.date_field] = parse(post[self.date_field])