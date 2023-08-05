"""Utilities to deploy/save Source files into the filesystem.

Ensuring that the folder hierarchy and the __init__.py files are in their place
is done in this module.
"""

import logging
import os
import os.path

__author__ = ['Alex Barcelo <alex.barcelo@bsc.es']
__copyright__ = '2016 Barcelona Supercomputing Center (BSC-CNS)'

logger = logging.getLogger(__name__)

# Almost hardcoded, but easily reachable... quite hacky, I know
MAGIC_LINE_NUMBER_FOR_IMPORTS = 14


def _ensure_package(package_path, ds_deploy):
    """Create the folder package_path and create the __init__.py file inside."""
    if not os.path.exists(package_path):
        os.mkdir(package_path)

    init_file = os.path.join(package_path, "__init__.py")
    if not os.path.exists(init_file):
        # logger.debug("Creating __init__.py file at folder %s", package_path)
        with open(init_file, 'w') as f:
            f.writelines([
                b"# Automatically created by dataClay\n",
                b"import os\n",
                b"import sys\n",
                b"\n",
                b"from dataclay.managers.classes import dclayMethod, dclayEmptyMethod, DataClayObject\n",
                b"from dataclay.contrib.dummy_pycompss import *\n",
                b"\n",
                b"from logging import getLogger\n",
                b"getLogger('dataclay.deployed_classes').debug('Package path: %s')\n" % package_path,
                b"StorageObject = DataClayObject\n",
                b"\n",
                b"###############################################################\n",
                b"######### <Class-based imports>:\n",
                b"\n",
                # Here the lines will be inserted, eventually, as needed (14th line at the moment)
                b"\n",
                b"######### </Class-based imports>\n",
                b"###############################################################\n",
            ])
            # ATTENTION! If you add any line to the previous header, update the variable
            # MAGIC_LINE_NUMBER_FOR_IMPORTS

            if ds_deploy:
                f.writelines([
                    b"\n",
                    b"from dataclay.contrib.dummy_pycompss import *\n",
                    b"\n",
                ])
            else:
                f.writelines([
                    # TODO: clean this up a little bit, and add the INOUT and similar typical imports
                    b"\n",
                    b"try:\n"
                    b"    from pycompss.api.task import task\n"
                    b"except ImportError:\n",
                    b"    from dataclay.contrib.dummy_pycompss import *\n",
                    b"\n",
                ])


def deploy_class(namespace, full_name, source, imports, source_deploy_path, ds_deploy=False):
    """Deploy a class source to the filesystem.

    :param namespace: The namespace of the class (first part of package name).
    :param full_name: The full name (including package) of the class.
    :param source: The Python's source code for the class.
    :param source_deploy_path: The root for deployed source code.
    :param ds_deploy: If true, that means that the deploy is for a DataService (not client)
    """
    _ensure_package(source_deploy_path, ds_deploy)

    package, klass = ("%s.%s" % (namespace, full_name)).rsplit('.', 1)
    # logger.info("Going to deploy class %s in path %s/__init__.py",
    #             klass, package.replace(".", "/"))

    current_path = source_deploy_path
    for p in package.split("."):
        current_path = os.path.join(current_path, p)
        _ensure_package(current_path, ds_deploy)

    class_path = os.path.join(current_path, "__init__.py")
    # logger.debug("Class destination file: %s", class_path)

    if not os.path.exists(class_path):
        raise IOError("__init__.py file in package %s should have been already initialized"
                      % package)
    else:
        # Because we need to insert imports in a nice place, read & write approach
        with open(class_path, 'r') as f:
            contents = f.readlines()

        contents = contents[:MAGIC_LINE_NUMBER_FOR_IMPORTS] \
                   + [imports] \
                   + contents[MAGIC_LINE_NUMBER_FOR_IMPORTS:] \
                   + [source]

        with open(class_path, 'w') as f:
            f.writelines(contents)
