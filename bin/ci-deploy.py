#!/usr/bin/env python
#

# Jenkins Job Manager

import argparse
import logging
import os
import pprint
import sys

import jenkins_jobs.config
import jenkins_jobs.cli
import jenkins_jobs.builder
import jenkins_jobs.cmd

utildir = os.path.dirname(__file__)
libdir = os.path.join(utildir, "lib")
sys.path.insert(0, libdir)

import jj.cli.deploy
import jj.modules


def get_options():
    parser = argparse.ArgumentParser()
    parser, _ = jenkins_jobs.cli.parse(parser, [])

    recursive_parser = argparse.ArgumentParser(add_help=False)
    recursive_parser.add_argument('-r', '--recursive', action='store_true',
                                  dest='recursive', default=False,
                                  help='look for python files recursively')
    recursive_parser.add_argument('-x', '--exclude', dest='exclude',
                                  action='append', default=[],
                                  help='paths to exclude when using recursive'
                                       ' search, uses standard globbing.')

    subparser = parser.add_subparsers(dest='command')
    jj.cli.deploy.parse(subparser, [recursive_parser])

    argv = sys.argv[1:]
    return parser.parse_args(argv)


def main():
    options = get_options()
    config = jenkins_jobs.config.load(options)
    builder, options, config = jenkins_jobs.cmd.munge_config_options(options,
                                                                     config)

    plugins_info = builder.plugins_list
    registry = jenkins_jobs.registry.ModuleRegistry(config, plugins_info)
    xml_builder = jenkins_jobs.xml_config.XmlBuilder(registry)

    modules = jj.modules.find_and_load_modules(options.module_path)

    jobs = []
    for module in modules:
        jobs.extend(module.get_jobs())

    xml_jobs = xml_builder.generateXML(jobs)

    pprint.pprint([j.output() for j in xml_jobs])
    pprint.pprint(jobs)


if __name__ == "__main__":
    main()
