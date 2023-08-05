from .baseclass import ManagementObject


class Interface(ManagementObject):
    _fields = ["dataClayID", 
               "providerAccountName",
               "namespace",
               "classNamespace",
               "className",
               "propertiesInIface",
               "operationsSignatureInIface",
               ]

    _internal_fields = ["providerAccountID",
                        "namespaceID",
                        "classNamespaceID",
                        "metaClassID",
                        "operationsIDs",
                        "propertiesIDs",
                        ]
