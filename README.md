# CI UX Experiments

The purpose of this project is to provide an example of how CI -could- be
configured.

## Configuration

Configuration under this system is determined by two levels of abstraction. At
the high-level we provide simple key-value mappings for each project that feed
into the lower-level as configuration parameters.

### High-level (aka "Dev-facing") UX

The user-facing "UX" has these goals:

* Provide simple interface for tweaking CI parameters
* Document how to perform common tasks
 * Modify default build parameters
 * Enable/Disable pipelines
 * Duplicate pipelines for new branches
 * Create pipelines for new projects

```
 pipelines
 ├── defaults.yaml
 ├── enterprise
 │   ├── defaults.yaml
 │   ├── node-management-services
 │   │   ├── activity-service.yaml
 │   │   ├── classifier.yaml
 │   │   ├── defaults.yaml
 │   │   └── rbac.yaml
 │   └── utility-jobs.yaml
 ├── modules
 ├── platform
 └── qe
```
Above is a directory hierarchy in which each directory contains its own set of
defaults that overrides and complements the previous directory. The override
order in the example of the classifier pipeline (lowest to highest priority) is:

* pipelines/defaults.yaml
* pipelines/enterprise/defaults.yaml
* pipelines/enterprise/node-management-services/defaults.yaml
* pipelines/enterprise/node-management-services/classifier.yaml

The contents of `pipelines/enterprise/node-management-services/classifier.yaml`
might look something like:

```yaml
github_repo: puppetlabs/classifier
prs_enabled: True
# ^-- parameters that apply for each pipeline shown below

pipelines:
    - 'composite-ezbake_v0':
        scm_branch: stable
        pe_family: 2015.3.x
        # ^-- parameters that apply only for this instance of
        # `composite-ezbake_v0`
```

Some important points to note:

* Parameters that are set project-wide are merged onto a copy of the defaults
  specified up to this level.
* Parameters that are set at the pipeline instance level are in turn merged onto
  the parameters set at the project-wide leve.

### Low-level (aka "QE-facing") UX

At the low level we have an object-oriented API that wraps around
programmatic configuration for a given CI system to provide a consistent
interface to be targeted by the "High-level" config parameters.

The low level API provides hooks to projects in the form of named pipelines that
are referenced at the pipeline level. For example, assume we have a Pipeline
defined in Python:

```python
class EZBakeCompositePipeline(MultiJobPluginPipeline):
    pipeline_name = 'composite-ezbake_v0'

    def __init__(self, name=None, **kwargs):
        self.configure_pipeline(**kwargs)

    def configure_pipeline(self, **kwargs):
        job1 = Job(...)
        job2 = Job(...)
        do_cool_stuff()

def define_pipeline(pipeline_registry):
    pipeline_registry.append(EZBakePipelineV0)
```

The name passed to that Pipeline, `composite-ezbake_v0` can then be referenced
in the high-level pipeline instantiation:

```yaml
github_repo: puppetlabs/classifier
prs_enabled: True

pipelines:
    - 'composite-ezbake_v0':
        scm_branch: stable
        pe_family: 2015.3.x
```

The parameters at the top level of this YAML file apply to all pipelines. Each
individual instance of the pipeline then adds its own parameters. All parameters
are merged to create a single dictionary passed to the Pipeline class above when
creating a concrete instance of its type.

## Tooling

Tooling should be focused around providing simple interfaces to perform common
development, testing, and deployment tasks.

### Development

During development of new pipelines, being provided a preview of the effect of
new changes allows developers

#### Visualize Job Relationships
```
./bin/ci-viz.py -r 
```
Generate a viz diagram of the 

### Testing

#### Compare Revisions
```
./bin/ci-compare-revisions.py
```


### Deployment

```
./bin/ci-deploy.py -p value_stream=experimental -p hipchat_room='${PROJECT_ROOM}' -c pipelines/enterprise/node-management-services/classifier.yaml
```
Deploy "experimental" copies of the Node Classifier pipelines from the current
working directory with the `hipchat_room` parameter overridden to direct
notifications to a low-traffic room.

```
./bin/ci-deploy.py -p git_branch=PE-11389 -r "enterprise_classifier_.*"
```
Deploy copies of pipelines targeting "PE-11389" branches. Filters deployed jobs using the given regex matched against the job name such that only classifer jobs are deployed.

