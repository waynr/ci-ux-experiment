import sys

from jj.job import Job
from jj.project import Project
from jj.pipeline import Pipeline


def get_jobs():
    j = Job({
        "name": "herp_derp_world"
        })

    return [j]
