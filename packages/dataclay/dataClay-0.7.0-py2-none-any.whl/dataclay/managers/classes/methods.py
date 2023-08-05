import logging
from decorator import decorate

from dataclay import runtime

__author__ = 'Alex Barcelo <alex.barcelo@bsc.es>'
__copyright__ = '2016 Barcelona Supercomputing Center (BSC-CNS)'

logger = logging.getLogger(__name__)


def _dclayMethod(f, self, *args, **kwargs):
    """Helper function for DataClayObject method decoration"""
    logger.debug("Calling function %s", f.__name__)

    if self._dclay_instance_extradata.loaded_flag or f._dclay_local or f.__name__.startswith("__dclay"):
        return f(self, *args, **kwargs)
    else:
        return runtime.execute_implementation_aux(f.__name__, self, args)


def _dclayEmptyMethod(f, self, *args, **kwargs):
    """Similar to dclayMethod, but without actual Python implementation."""
    logger.debug("Calling (languageless) function %s", f.__name__)

    # Let it fail elsewhere, if the user hacks around into an invalid state
    # (like a loaded&local non-persistent instance with an dclayEmptyMethod,
    #  something that should not happen normally)
    return runtime.execute_implementation_aux(f.__name__, self, args)


class dclayMethod(object):
    """Class-based decorator for DataClayObject method decoration"""
    def __init__(self, **kwargs):
        """Provide the argument type information

        The programmer is expected to set the same kwargs as the function,
        in addition to the `return_` special method return type.

        The typical usage is:

            @dclayMethod(a=int,
                         b='some.path.to.Class',  # this is valid (str)
                         c=imported.path.to.Class, # this is also valid
                         return_=None)
            def foo_bar(a, b, c):
                ...

        The method should be inside a DataClayObject derived class. See both
        DataClayObject class implementation and ExecutionGateway metaclass for
        more information about the internal behaviour.
        """
        self._method_args = kwargs

    def __call__(self, f):
        logger.debug('Preparing dataClay method `%s` with arguments: %s',
                     f.func_name, self._method_args)
        decorated_func = decorate(f, _dclayMethod)
        decorated_func._dclay_entrypoint = f
        decorated_func._dclay_ret = self._method_args.pop("return_", None)
        decorated_func._dclay_args = self._method_args
        decorated_func._dclay_method = True

        # Store the local flag in both the function and the decorated function
        is_local = self._method_args.pop("_local", False)
        f._dclay_local = is_local
        # TODO: at the moment, this flag is ignored
        decorated_func._dclay_local = is_local

        # ToDo: something more clever, or add the user-provided flag option at least
        decorated_func._dclay_readonly = False
        return decorated_func


def dclayEmptyMethod(f):
    """Simple (parameter-less) decorator for languageless methods."""
    decorated_func = decorate(f, _dclayEmptyMethod)
    decorated_func._dclay_method = True
    # ToDo: something more clever, or add the user-provided flag option at least
    decorated_func._dclay_readonly = False
    return decorated_func
