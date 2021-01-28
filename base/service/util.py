from enum import Enum
from pprint import PrettyPrinter
from sys import stdout
import netifaces
from datetime import datetime
from typing import Union
from functools import reduce
from os import environ, getenv

# Enums

class HttpVerb(str, Enum):
    """
    usage:
        HttpVerb.get
    """
    get = 'get'
    put = 'put'
    patch = 'patch'
    post = 'post'
    delete = 'delete'

class TimeUnit(str, Enum):
    """
    usage:
        TimeUnit.minute
    """
    day = 'day'
    hour = 'hour'
    minute = 'minute'
    second = 'second'

# functions

def all_visible_subclasses(klass):
    def helper(klas, result):
        subklases = klas.__subclasses__()
        if len(subklases) > 0:
            result.update(subklases)
            for subklas in subklases:
                helper(subklas, result)
    result = set()
    helper(klass, result)
    return result

def key_strings_from_class(klass):
    return set(x for x in klass.__fields__.keys())

def key_strings_from_dict(dictionary:dict):
    return set(x for x in dictionary)

def resolve_instance(klass, dictionary:dict):
    dictionary_keys = key_strings_from_dict(dictionary)
    subclasses = all_visible_subclasses(klass)
    min_count = 100
    selected_subclass = None
    for subclass in subclasses:
        class_keys = key_strings_from_class(subclass)
        if len(dictionary_keys-class_keys) == 0:
            count = len(class_keys)
            if count<min_count:
                selected_subclass = subclass
                min_count = count
    return selected_subclass(**dictionary) if selected_subclass else None

def object_info(obj):
    return {
        'class': f"{obj.__class__.__module__}.{obj.__class__.__name__}",
        'instance': obj
    }

# classes

class ResolveBody:
    def __init__(self, klass):
        self.klass = klass
    def __call__(self, body:dict):
        if body:
            return resolve_instance(self.klass, body)
        return None



def subclass_union(klass):
    """
    usage:
    union_of_subclasses_of_Action = subclass_union(base.Action)
    note:
    superceded by resolve_instance & ResolveBody in FastAPI path dependencies
    """
    return reduce(lambda a, b=None: Union[b,a], all_visible_subclasses(klass))


class Now:
    @classmethod
    def s(cls):
        now = cls.dt()
        return f"{now.strftime('%H:%M:%S')} on {now.strftime('%Y-%m-%d')}"
    @classmethod
    def dt(cls):
        return datetime.now()
    @classmethod
    def t(cls):
        return cls.dt().time()



class Output:
    """
    usage:
    Output.pprint({'a', 'abc'}, ('debug', Output.debug()))
    """
    @classmethod
    def debug(cls):
        return 'debug', Dirs.output_dir()

    @classmethod
    def pprint(cls, lev_fil:tuple[str,str], dictionary:dict):
        level, file = lev_fil
        with open(file, 'a') as outfile:
            something = {'level':level}
            something.update(dictionary)
            PP.pprint(something, stream=outfile)

class PP:
    """
    usage:
        PP.pprint(json_ish_object)
    note:
        could be a function, but PP asserts its global nature
    """
    @classmethod
    def pprint(cls, dictionary, indent=2, stream=stdout):
        PrettyPrinter(indent=indent, stream=stream).pprint(dictionary)

class IP:
    """
    usage:
        IP.addr
    note:
        singleton
    lineage:
        from netifaces import interfaces, ifaddresses, AF_INET
        for ifaceName in interfaces():
            addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
            print ('%s: %s' % (ifaceName, ', '.join(addresses)))
    """
    addr = "need a fix for linux"#netifaces.ifaddresses('en0').setdefault(netifaces.AF_INET)[0]['addr']
    @classmethod
    def reset(cls):
        cls.addr = "need a fix for linux"#netifaces.ifaddresses('en0').setdefault(AF_INET)[0]['addr']

class Dirs:
    output_label, output_default_dir = 'PYRAMBIUM_OUTPUT_DIR', '/tmp/pyrambium/output/'
    saved_label, saved_default_dir = 'PYRAMBIUM_SAVED_DIR', '/tmp/pyrambium/saved/'
    @classmethod
    def compute_dir(cls, label, default_dir):
        dir = getenv(label)
        if not dir:
            dir = default_dir
            environ[label] = dir
        return dir
    @classmethod
    def output_dir(cls):
        return cls.compute_dir(cls.output_label, cls.output_default_dir)
    @classmethod
    def saved_dir(cls):
        return cls.compute_dir(cls.saved_label, cls.saved_default_dir)