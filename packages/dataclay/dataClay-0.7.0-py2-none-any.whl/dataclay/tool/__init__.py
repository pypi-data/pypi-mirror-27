"""dataClay Tool code for Python.

The code in this package is intended to be used by the "dataClay Tool", for all
the Python specific stuff.
"""

# TODO The below code should be deprecated as soon as the dclayTool.sh is done

import os
import sys
from uuid import UUID
from importlib import import_module

from dataclay.api import init_connection, finish
from dataclay import runtime, management
from dataclay.core import constants

from jinja2 import Template
import yaml
import grpc

from dataclay.core.constants import lang_codes
from dataclay.managers.classes import ExecutionGateway
from dataclay.managers.classes.factory import MetaClassFactory

__author__ = 'Alex Barcelo <alex.barcelo@bsc.es>'
__copyright__ = '2017 Barcelona Supercomputing Center (BSC-CNS)'


USAGE_TEXT = """
Current commands:

    ./manage.py createuser <admin_user> <admin_password> <new_user> <new_user_password>
    
Creates a user. Needs to be provided admin credentials in order to perform
the operation.

    ./manage.py registertodataclaypubliccontract <user> <password>
    
Prepares a contract to the dataClay public classes (aka dc_classes, aka contrib
classes).  If the namespace doesn't exist, it will be created.

    ./manage.py registermodule <namespace> <module_name> <user> <password>

Register a whole "model" folder, in which there are multiple classes and packages.
If the namespace doesn't exist, it will be created.

    ./manage.py __new__registermodel <namespace> <python_path> <user> <password>
    
Registers all StorageObject classes in a certain module (relative to the
current folder). The classes are registered onto the provided namespace
(created if non-existent).

A full default contract for all registered classes is created and its 
ContractID is returned.

The user credentials should be provided (a "registrator" kind of user).

    ./manage.py registerdataset <dataset> <user> <password>

Creates a dataset and also its matching datacontract. The creation user and
usage user is the same (provided user and password).

    ./manage.py getstubs <contract_ids> <path> <user> <password>
    
Given a ContractID (or a comma-separated list of ContractIDs) download its 
stubs into the provided path. The user should already have a contract to 
access those classes.
"""

def _execute_from_command_line(argv=None):
    client = runtime.ready_clients["@LM"]

    if len(argv) < 2:
        print >> sys.stderr, "You should provide a command to the tool."
        print >> sys.stderr, USAGE_TEXT
        return

    # ToDo: A smarter strategy should be used here. At the moment, all commands
    # ToDo: are hardcoded and behaviour is programmed somewhat ad hoc.
    if argv[1] == "createuser":
        # Create a NORMAL_ROLE user.

        admin_id = client.get_account_id(argv[2])
        admin_credential = (None, argv[3])
        username = argv[4]
        password = argv[5]

        yaml_request_template = Template("""
---
 - !!util.management.accountmgr.Account
   username: {{ username }}
   credential: !!util.management.accountmgr.PasswordCredential
     password: {{ password }}
   role: NORMAL_ROLE
""")

        yaml_request = yaml_request_template.render(
            username=username,
            password=password,
        )

        client.perform_set_of_new_accounts(admin_id,
                                           admin_credential,
                                           yaml_request)

    elif argv[1] == "registertodataclaypubliccontract":
        username = argv[2]
        credential = (None, argv[3])

        user_id = client.get_account_id(username)

        #########################################################################
        # First, we prepare the namespace:

        try:
            namespace_id = client.get_namespace_id(user_id, credential, "dc_classes")
        except Exception:
            yaml_request = """
---
{namespace}: !!util.management.namespacemgr.Namespace
    providerAccountName: {consumer_name}
    name: {namespace_name}
    language: LANG_PYTHON
""".format(consumer_name=username,
           namespace="dc_classes",
           namespace_name="dc_classes")

            yaml_response = client.perform_set_of_operations(user_id, credential, yaml_request)
            response = yaml.load(yaml_response)

            namespace_id = response["namespaces"]["dc_classes"]

        #########################################################################
        # Then we prepare the classes
        from dataclay import contrib
        modules = contrib.MODULES_TO_REGISTER

        mfc = MetaClassFactory(namespace="dc_classes",
                               responsible_account=username)

        for m_str in modules:
            m = import_module("dataclay.contrib.%s" % m_str)

            for c_str in getattr(m, "CLASSES_TO_REGISTER"):
                mfc.add_class(getattr(m, c_str))

        client = runtime.ready_clients["@LM"]
        result = client.new_class(user_id, credential, lang_codes.LANG_PYTHON, mfc.classes)

        if not result:
            raise RuntimeError("No classes successfully registered --cannot continue")

        class_interface_template = Template("""
{{ brief_name }}interface: &{{ brief_name }}iface !!util.management.interfacemgr.Interface
  providerAccountName: {{ username }}
  namespace: dc_classes
  classNamespace: dc_classes
  className: {{ class_name }}
  propertiesInIface: !!set {% if class_info.properties|length == 0 %} { } {% endif %}
  {% for property in class_info.properties %}
    ? {{ property.name }}
  {% endfor %}
  operationsSignatureInIface: !!set {% if class_info.operations|length == 0 %} { } {% endif %}
  {% for operation in class_info.operations %}
    ? {{ operation.nameAndDescriptor }}
  {% endfor %}
""")

        class_interface_in_contract_template = Template("""
    - !!util.management.contractmgr.InterfaceInContract
      iface: *{{ brief_name }}iface
      implementationsSpecPerOperation: !!set {% if class_info.operations|length == 0 %} { } {% endif %}
        {% for operation in class_info.operations %}
          ? !!util.management.contractmgr.OpImplementations
            operationSignature: {{ operation.nameAndDescriptor }}
            numLocalImpl: 0
            numRemoteImpl: 0
        {% endfor %}
    """)

        classes_render = list()
        incontract_render = list()
        for class_name, class_info in result.items():
            brief_name = class_name.rsplit(".", 1)[-1].lower()
            classes_render.append(class_interface_template.render(
                username=username,
                brief_name=brief_name,
                class_name=class_name,
                class_info=class_info))
            incontract_render.append(class_interface_in_contract_template.render(
                brief_name=brief_name, class_info=class_info
            ))

        yaml_request_template = Template("""
---
{% for class_iface in class_interfaces %}
{{ class_iface }}
{% endfor %}
contribcontract: !!util.management.contractmgr.Contract
  beginDate: 2012-09-10T20:00:03
  endDate: 2020-09-10T20:00:04
  namespace: dc_classes
  providerAccountName: {{ username }}
  applicantsNames:
    ? {{ username }}
  interfacesInContractSpecs:
    {% for contract in contracts %}
    {{ contract }}
    {% endfor %}
  publicAvailable: True
""")
        yaml_request = yaml_request_template.render(
            username=username,
            class_interfaces=classes_render,
            contracts = incontract_render
        )

        yaml_response = client.perform_set_of_operations(user_id, credential, yaml_request)
        response = yaml.load(yaml_response)

        #########################################################################
        # Now (hopefully) the contract for the public classes has been obtained
        print >> sys.stderr, " ===> The ContractID for the registered classes is:",
        print response["contracts"]["contribcontract"]

    elif argv[1] == "__new__registermodel":
        namespace = argv[2]
        python_path = argv[3]
        username = argv[4]
        password = argv[5]

        # Ugly stuff related to the namespace first...
        credential = (None, password)
        user_id = client.get_account_id(username)

        yaml_request_template = Template("""
---
{{ namespace }}: !!util.management.namespacemgr.Namespace
  providerAccountName: {{ username }}
  name: {{ namespace }}
  language: LANG_PYTHON
""")
        yaml_request = yaml_request_template.render(
            namespace=namespace,
            username=username
        )

        try:
            client.perform_set_of_operations(user_id, credential, yaml_request)
        except grpc.RpcError:
            # We assume that the namespace already exists
            pass

        # Then use the new register_model shiny stuff
        from .functions import register_model
        register_model(namespace=namespace,
                       python_path=python_path,
                       username=username,
                       password=password)

    elif argv[1] == "registermodule":
        namespace = argv[2]
        module_name = argv[3]
        username = argv[4]
        credential = (None, argv[5])

        user_id = client.get_account_id(username)

        yaml_request_template = Template("""
---
{{ namespace }}: !!util.management.namespacemgr.Namespace
  providerAccountName: {{ username }}
  name: {{ namespace }}
  language: LANG_PYTHON
""")
        yaml_request = yaml_request_template.render(
            namespace=namespace,
            username=username
        )

        try:
            client.perform_set_of_operations(user_id, credential, yaml_request)
        except grpc.RpcError:
            # We assume that the namespace already exists
            pass

        mfc = MetaClassFactory(namespace=namespace,
                               responsible_account=username)

        # Scrap the classes in the module
        registered_classes = list()
        module = import_module(module_name)
        for thing_name in dir(module):
            thing = getattr(module, thing_name)

            if not isinstance(thing, ExecutionGateway):
                continue

            # Thing seems to be a DataClayObject class
            if thing.__module__ != module_name:
                print >> sys.stderr, "The module for %s is %s, ignoring because it does not equals %s" % (
                    thing, thing.__module__, module_name
                )
                continue

            # Ok, that's a valid class
            mfc.add_class(thing)
            registered_classes.append(thing.__name__)

        registrator_id = client.get_account_id(username)
        result = client.new_class(registrator_id,
                                  credential,
                                  constants.lang_codes.LANG_PYTHON,
                                  mfc.classes)

        print >> sys.stderr, "Was gonna register: %s\nEventually registered: %s" % (
            registered_classes, result.keys())

        if len(result.keys()) == 0:
            print >> sys.stderr, "No classes registered, exiting"
            return

        interfaces = list()
        interfaces_in_contract = list()

        for class_name, class_info in result.iteritems():
            ref_class_name = class_name.replace('.', '')

            interfaces.append(Template("""
{{ class_name }}interface: &{{ ref_class_name }}iface !!util.management.interfacemgr.Interface
  providerAccountName: {{ username }}
  namespace: {{ namespace }}
  classNamespace: {{ namespace }}
  className: "{{ reg_class_name }}"
  propertiesInIface: !!set {% if class_info.properties|length == 0 %} { } {% endif %}
  {% for property in class_info.properties %}
     ? {{ property.name }}
  {% endfor %}
  operationsSignatureInIface: !!set {% if class_info.operations|length == 0 %} { } {% endif %}
  {% for operation in class_info.operations %} 
    ? {{ operation.nameAndDescriptor }}
  {% endfor %}
""").render(
                class_name=ref_class_name,
                reg_class_name=class_name,
                username=username,
                namespace=namespace,
                class_info=class_info))

            interfaces_in_contract.append(Template("""
    - !!util.management.contractmgr.InterfaceInContract
      iface: *{{ class_name }}iface
      implementationsSpecPerOperation: !!set {% if class_info.operations|length == 0 %} { } {% endif %}
        {% for operation in class_info.operations %}
          ? !!util.management.contractmgr.OpImplementations
            operationSignature: {{ operation.nameAndDescriptor }}
            numLocalImpl: 0
            numRemoteImpl: 0
        {% endfor %}
""").render(
                class_name=ref_class_name,
                class_info=class_info))

        contract = Template("""
{{ namespace }}contract: !!util.management.contractmgr.Contract
  beginDate: 1980-01-01T00:00:01
  endDate: 2055-12-31T23:59:58
  namespace: {{ namespace }}
  providerAccountName: {{ username }}
  applicantsNames:
    ? {{ username }}
  interfacesInContractSpecs:
{{ interfaces_in_contract }}
  publicAvailable: True
""").render(
            namespace=namespace,
            username=username,
            interfaces_in_contract="\n".join(interfaces_in_contract)
        )

        yaml_request = "\n".join(interfaces) + contract
        print >> sys.stderr, " ===> The yaml for performing is %s" % (yaml_request)

        yaml_response = client.perform_set_of_operations(user_id, credential, yaml_request)
        response = yaml.load(yaml_response)

        print >> sys.stderr, " ===> The ContractID for the registered classes is: ",
        print response["contracts"]["%scontract" % namespace]

    elif argv[1] == "registerdataset":
        dataset = argv[2]
        username = argv[3]
        credential = (None, argv[4])

        user_id = client.get_account_id(username)

        yaml_request_template = Template("""
{{ dataset }}: !!util.management.datasetmgr.DataSet
  providerAccountName: {{ username }}
  name: {{ dataset }}

{{ dataset }}datacontract: !!util.management.datacontractmgr.DataContract
  beginDate: 1980-01-01T00:00:01
  endDate: 2055-12-31T23:59:58
  providerAccountName: {{ username }}
  dataSetProvidedName: {{ dataset }}
  applicantsNames:
    ? {{ username }}
  publicAvailable: True
""")
        yaml_request = yaml_request_template.render(
            dataset=dataset,
            username=username
        )

        try:
            client.perform_set_of_operations(user_id, credential, yaml_request)
        except grpc.RpcError as e:
            print >> sys.stderr, "Tried to do that operation and received: %s" % e

    elif argv[1] == "getstubs":
        contract_ids = map(UUID, argv[2].split(','))
        path = argv[3]
        username = argv[4]
        credential = (None, argv[5])

        user_id = client.get_account_id(username)

        management.prepare_storage(path)

        babel_data = client.get_babel_stubs(user_id,
                                            credential,
                                            contract_ids)

        with open(os.path.join(path, "babelstubs.yml"), 'wb') as f:
            f.write(babel_data)

        all_stubs = client.get_stubs(user_id, credential,
                                     constants.lang_codes.LANG_PYTHON,
                                     contract_ids)

        for key, value in all_stubs.iteritems():
            with open(os.path.join(path, key), 'wb') as f:
                f.write(value)

        management.deploy_stubs(path)
    else:
        print >> sys.stderr, "Unknown command."
        print >> sys.stderr, USAGE_TEXT
        return


def execute_from_command_line(argv=None):
    """Given the calling arguments to the manage.py script, do stuff.

    :param argv: Typically, sys.argv. Should be explicitly set by caller.
    :return: Nothing.
    """
    # Perform implicit initialization of connections (client.properties only, no storage.properties)
    client_properties_path = os.getenv("DATACLAYCLIENTCONFIG", "./cfgfiles/client.properties")
    assert client_properties_path, "dataclay.tool module can only be called with DATACLAYCLIENTCONFIG set"
    init_connection(client_properties_path)

    _execute_from_command_line(argv)

    # Do the cleanup to avoid __del__ messages of gRPC library
    finish()
