import collections
import imp
import importlib
import inspect
import os
import sys
import traceback


def find_and_load_modules(module_path):
    """
    Given a list of paths, recurse into those paths, load all python modules
    found, and return those that contain functions pertinent to JJB data
    structure loading.
    """

    modules = [m for m in __load_modules(module_path) if __is_valid(m)]

    return modules


def __load_modules(module_path):
    loaded_modules = []
    module_files = []

    for dirpath, dirnames, filenames in os.walk(module_path):
        relative_path = os.path.relpath(dirpath, module_path)
        if relative_path == ".":
            relative_path = ""
        for filename in filenames:
            name, ext = os.path.splitext(filename)
            if (ext == ".py" and not name == "__init__"):
                relative_path = ".".join(relative_path.split("/"))
                if relative_path == "":
                    module_files.append(name)
                else:
                    module_files.append(relative_path + "." + name)

    sys.path.insert(0, module_path)

    for module_file in module_files:
        loaded_modules.append(importlib.import_module(module_file))

    # avoid accidentially prioritizing some module in the jobs module path over
    # those defined elsewhere
    sys.path.remove(module_path)

    return loaded_modules


def __is_valid(module):
    """
    Perform basic validity check to ensure that the given module is compatible
    with the expectations we have for modules which generate JJB data
    structures.
    """

    if not inspect.ismodule(module):
        return False

    members = collections.OrderedDict(inspect.getmembers(module))

    if "get_jobs" not in members:
        return False

    return True
