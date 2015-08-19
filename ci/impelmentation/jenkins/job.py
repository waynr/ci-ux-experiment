#!/usr/bin/env python
#

# Jenkins Job Manager


class Job(dict):
    """ Base Jenkins Job class
    """

    def __init__(self, *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)
