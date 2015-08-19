#!/usr/bin/env python
#

# Jenkins Job Manager


class Project(object):
    """ Base Jenkins Job class
    """

    def __init__(self, name, **kwargs):
        self.name = name
