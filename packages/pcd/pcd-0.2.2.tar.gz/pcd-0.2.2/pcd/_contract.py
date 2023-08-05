## INFO ##
## INFO ##
"""
pcd - Python Contract Decorator
-------------------------------
Copyright (C) 2017 Peter Varo <hello@petervaro.com>

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along
with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from inspect     import getargspec
from collections import OrderedDict
# TODO: Consider switching to Decompyle++ https://github.com/zrax/pycdc for
#       more reliable Python3 support
from uncompyle6  import PYTHON_VERSION, deparse_code
try:
    from cStringIO import StringIO
    from itertools import izip as zip
except ModuleNotFoundError:
    from io import StringIO

__all__ = 'contract',

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# HACK: There is no reliable way to differentiate between a function and a
#       lambda expression, hence this hack which gets the name representation of
#       the object.  It is a hack, because the __name__ attribute can be
#       overridden, however that case is also handled since in that scenario,
#       the condition will be treated as a regular function, and the name will
#       be displayed instead of the uncompiled content of the lambda expression
_LAMBDA_NAME = (lambda: None).__name__


#------------------------------------------------------------------------------#
def prepare_conditions(conditions,
                       conditions_type,
                       function_name):
    # Make conditions iterable if they are not
    conditions = (conditions,) if callable(conditions) else conditions

    # Compose messages
    composed = OrderedDict()
    for condition in conditions:
        # Get source from bytecode if it is an anonym function
        if condition.__name__ == _LAMBDA_NAME:
            condition_repr = StringIO()
            deparse_code(PYTHON_VERSION,
                         condition.__code__,
                         out=condition_repr).text
            # Remove 'return '
            condition_repr = condition_repr.getvalue()[7:]
        # Use the validator name
        else:
            condition_repr = condition.__name__

        # Create assertion error message
        composed[condition] = 'in {}: {}: {}'.format(function_name,
                                                     conditions_type,
                                                     condition_repr)
    return composed


#------------------------------------------------------------------------------#
def _inject_invoke(assumption,
                   new_globals,
                   message,
                   takes_args = False,
                   result     = None):
    # Store original globals values and save new ones
    assumption_globals = assumption.__globals__
    old_globals = {}
    for variable, value in new_globals.items():
        try:
            old_globals[variable] = assumption_globals[variable]
        except KeyError:
            pass
        assumption_globals[variable] = value

    # Invoke validator
    try:
        if takes_args:
            assert assumption(result), message
        else:
            assert assumption(), message
    finally:
        # Restore original global values
        assumption_globals.update(old_globals)


#------------------------------------------------------------------------------#
def contract(pre  = (),
             post = (),
             mut  = ()):
    def decorator(function):
        # Prepare assumptions
        func_name = function.__name__
        prepared_pre  = prepare_conditions(pre, 'precondition', func_name)
        prepared_post = prepare_conditions(post, 'postcondition', func_name)
        prepared_mut  = prepare_conditions(mut, 'mutated-condition', func_name)

        # Strore function related information
        (function_args,
         function_varargs,
         function_keywords,
         function_defaults) = getargspec(function)
        function_args = function_args or ()
        function_defaults = dict(zip(reversed(function_args),
                                     reversed(function_defaults or ())))

        # Create new guarded function
        def wrapper(*args, **kwargs):
            # Construct arguments and store them as global variables in the
            # assumption-function's scope
            args_   = list(args)
            kwargs_ = kwargs.copy()
            new_globals = {}
            for function_arg in function_args:
                # If argument passed as a keyword argument
                try:
                    new_globals[function_arg] = kwargs_.pop(function_arg)
                    continue
                except KeyError:
                    pass

                # If argument passed as a positional argument
                try:
                    new_globals[function_arg] = args_.pop(0)
                    continue
                except IndexError:
                    pass

                # If argument not passed but has default value
                try:
                    new_globals[function_arg] = function_defaults[function_arg]
                    continue
                except KeyError:
                    pass

            # If catch-all positional arguments defined then set as the rest of
            # the passed positional arguments
            if function_varargs is not None:
                new_globals[function_varargs] = args_
            # If catch-all keyword arguments defined then set as the rest of the
            # passed keyword arguments
            if function_keywords is not None:
                new_globals[function_keywords] = kwargs_

            # Validate preconditions
            for assumption, message in wrapper.__conditions['pre'].items():
                _inject_invoke(assumption, new_globals, message)

            # Call the contract'd function
            result = function(*args, **kwargs)

            # Validate postconditions
            for assumption, message in wrapper.__conditions['post'].items():
                _inject_invoke(assumption, new_globals, message, True, result)

            # Validate mutated postcoditions
            for assumption, message in wrapper.__conditions['mut'].items():
                _inject_invoke(assumption, new_globals, message)

            # Return from the contract'd function
            return result

        # Store conditions for extensibility
        wrapper.__conditions = {'pre'  : prepared_pre,
                                'post' : prepared_post,
                                'mut'  : prepared_mut}
        return wrapper
    return decorator
