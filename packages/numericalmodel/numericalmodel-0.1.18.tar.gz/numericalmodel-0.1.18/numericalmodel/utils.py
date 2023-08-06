#!/usr/bin/env python3
# system modules
import logging
import warnings
import inspect
import re
import datetime
import collections
import itertools
import csv

# internal modules

# external modules
import numpy as np


######################
### util functions ###
######################
def read_csv(f, *args, **kwargs):
    """
    Read CSV from file and return a dict

    Args:
        f (filehandle): file handle
        args, kwargs: arguments passed to :any:`csv.DictReader`

    Returns:
        dict : keys are column names, values are column data
    """
    d = {}
    csvreader = csv.DictReader(f, *args, **kwargs)

    def tofloat(x):
        try:
            return float(x)
        except ValueError:
            return x
    d = dictlist_to_listdict(csvreader, fun=tofloat)
    return d


def write_csv(f, d, headersortkey=lambda x: x, *args, **kwargs):
    """
    Write CSV dict to file

    Args:
        f (filehandle): writeable file handle
        headersortkey (callable): ``key`` argument to :any:`sorted` to sort the
            header columns
        args, kwargs: arguments passed to :any:`csv.DictWriter`
    """
    csvwriter = csv.DictWriter(
        f, fieldnames=sorted(d.keys(), key=headersortkey), *args, **kwargs)
    l = listdict_to_dictlist(d)
    csvwriter.writeheader()
    for row in l:
        csvwriter.writerow(row)


def listdict_to_dictlist(d):
    """
    Convert a :any:`dict` of lists to a list of dicts

    Args:
        d (dict): the dict of lists

    Returns:
        list : list of dicts
    """
    return [dict(zip(d, t)) for t in zip(*d.values())]


def dictlist_to_listdict(l, fun=lambda x: x):
    """
    Convert a list of dicts to a dict of lists

    Args:
        l (list): the list of dicts
        fun (callable): callable to manipulate the values

    Returns:
        dict : dict of lists
    """
    d = collections.defaultdict(list)
    for e in l:
        for k, v in e.items():
            d[k].append(fun(v))
    return dict(d)


def is_numeric(x):
    """
    Check if a given value is numeric, i.e. whether numeric operations can be
    done with it.

    Args:
        x (any): the input value

    Returns:
        bool: ``True`` if the value is numeric, ``False`` otherwise
    """
    attrs = ['__add__', '__sub__', '__mul__', '__truediv__', '__pow__']
    return all(hasattr(x, attr) for attr in attrs)


def utcnow():
    """
    Get the current utc unix timestamp, i.e. the utc seconds since 01.01.1970.

    Returns:
        float : the current utc unix timestamp in seconds
    """
    ts = (datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)
          ).total_seconds()
    return ts


def rmse(a, b):
    """
    RMSE (root mean squared error)
    """
    return np.sqrt(np.mean((a - b)**2))


def multi_rmse(*args):
    """
    RMSE (root mean squared error) for more than 2 elements
    """
    return np.mean([rmse(a, b) for a, b in itertools.combinations(args, 2)])

####################
### util classes ###
####################


class ReprObject(object):
    """
    Simple base class that defines a :any:`__repr__` method based on an object's
    ``__init__`` arguments and properties that are named equally. Subclasses of
    :any:`ReprObject` should thus make sure to have properties that are named
    equally as their ``__init__`` arguments.
    """
    @classmethod
    def _full_variable_path(cls, var):
        """ Get the full string of a variable

        Args:
            var (any): The variable to get the full string from

        Returns:
            str : The full usable variable string including the module
        """
        if inspect.ismethod(var):  # is a method
            string = "{module}.{cls}.{name}".format(
                name=var.__name__, cls=var.__self__.__class__.__name__,
                module=var.__module__)
        else:
            name = var.__name__
            module = var.__module__
            if module == "builtins":
                string = name
            else:
                string = "{module}.{name}".format(name=name, module=module)
        return(string)

    def __repr__(self):
        """
        Python representation of this object

        Returns:
            str : a Python representation of this object based on its
            ``__init__`` arguments and corresponding properties.
        """
        indent = "    "
        # the current "full" classname
        classname = self._full_variable_path(self.__class__)

        # get a dict of {'argname':'property value'} from init arguments
        init_arg_names = inspect.getfullargspec(self.__init__).args
        init_args = {}  # start with empty dict
        for arg in init_arg_names:
            if arg == "self":
                continue  # TODO hard-coded 'self' is bad
            try:
                attr = getattr(self, arg)  # get the attribute
                try:
                    string = self._full_variable_path(attr)
                except BaseException:
                    string = repr(attr)

                # indent the arguments
                init_args[arg] = re.sub(
                    string=string,
                    pattern="\n",
                    repl="\n" + indent,
                )
            except AttributeError:  # no such attribute
                warnstr = (
                    "class {cls} has no property or attribute "
                    "'{arg}' like the argument in its __init__. Cannot include "
                    "argument '{arg}' into __repr__.").format(
                    cls=classname, arg=arg)
                warnings.warn(warnstr)

        # create "arg = {arg}" string list for reprformat
        args_kv = []
        for arg in init_args.keys():
            args_kv.append(indent + "{arg} = {{{arg}}}".format(arg=arg))

        # create the format string
        if args_kv:  # if there are arguments
            reprformatstr = "\n".join([
                "{____classname}(", ",\n".join(args_kv), indent + ")", ])
        else:  # no arguments
            reprformatstr = "{____classname}()"

        # add classname to format args
        reprformatargs = init_args.copy()
        reprformatargs.update({"____classname": classname})

        reprstring = (reprformatstr).format(**reprformatargs)
        return reprstring


class SetOfObjects(ReprObject, collections.MutableMapping):
    """
    Base class for sets of objects
    """

    def __init__(self, elements=[], element_type=object):
        self.store = dict()  # empty dict

        # set properties
        self.element_type = element_type
        self.elements = elements

    ##################
    ### Properties ###
    ##################
    @property
    def elements(self):
        """
        return the list of values

        :getter:
            get the list of values
        :setter:
            set the list of values. Make sure, every element in the list is an
            instance of (a subclass of) :any:`element_type`.
        :type: :any:`list`
        """
        return [self.store[x] for x in sorted(self.store)]

    @elements.setter
    def elements(self, newelements):
        assert isinstance(newelements, collections.Iterable), (
            "elements have to be list")
        # re-set the dict and fill it with new data
        tmp = dict()  # temporary empty dict
        for i, elem in enumerate(newelements):
            assert self.element_type(elem), \
                "new element nr. {} does not match type".format(i)
            key = self._object_to_key(elem)  # get the key
            assert key not in tmp, \
                "element '{}' present multiple times".format(key)
            tmp.update({key: elem})  # add to temporary dict

        self.store = tmp.copy()  # set internal dict

    @property
    def element_type(self):
        """
        Function to check if a given element is okay. Takes the new element as
        single argument and returns ``True`` if yes, ``False`` otherwise.

        :setter: If set to a class, it is set to ``lambda x:
            isisntance(x,class)``
        """
        try:
            self._element_type
        except AttributeError:
            self._element_type = lambda x: True  # default
        return self._element_type

    @element_type.setter
    def element_type(self, newtype):
        f = (lambda x: isinstance(x, newtype)) \
            if inspect.isclass(newtype) else newtype
        assert hasattr(f, "__call__"), "element_type has to be callable"
        self._element_type = f

    ###############
    ### Methods ###
    ###############
    def _object_to_key(self, obj):
        """ key transformation function. Subclasses should override this.

        Args:
            obj (object): object

        Returns:
            str : the unique key for this object. Defaults to ``repr(obj)``
        """
        return repr(obj)  # by default, return the object's repr

    def add_element(self, newelement):
        """
        Add an element to the set

        Args:
            newelement : the new element
        """
        tmp = self.elements.copy()  # TODO does this destroy references?
        tmp.append(newelement)
        self.elements = tmp

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        assert self.element_type(value), "new value does not match type"
        self.store[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __getattr__(self, attr):
        if attr in self:
            return self[attr]
        else:
            raise AttributeError("'{}' object has no attribute '{}'".format(
                self.__class__.__name__, attr))

    def __str__(self):  # pragma: no cover
        """
        Stringification

        Returns:
            str : a summary
        """
        string = "\n\n".join(str(x) for x in self.elements)
        if string:
            return string
        else:
            return "none"
