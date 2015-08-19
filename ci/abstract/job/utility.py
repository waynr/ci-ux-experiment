from jj.job import Job
from jj.project import Project
from jj.pipeline import Pipeline


def get_jobs():
    j = Job({
        "name": "hello-world",
        "display-name": "hello-world",
        "project-type": "freestyle"
        })

    return [j]
