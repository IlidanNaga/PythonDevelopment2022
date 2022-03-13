import sys
import inspect
from importlib import import_module
from ast import parse, walk, unparse
from difflib import SequenceMatcher
from textwrap import dedent

container = dict()
remove_attrs = ['name', 'id', 'arg', 'attr']


def recursive_selection(prev_name, prev_object):
    
    for name, object in inspect.getmembers(prev_object):
        
        if inspect.isclass(object):
            
            if name[:2] != "__":
                recursive_selection(prev_name + "." + name, object)
        
        elif inspect.ismethod(object) or inspect.isfunction(object):
            src = dedent(inspect.getsource(object))
            ast_tree = parse(src)
            
            for node in walk(ast_tree):
                
                for attr in remove_attrs:
                    if hasattr(node, attr):
                        setattr(node, attr, "_")
            
            container[prev_name + "." + name] = unparse(ast_tree)


for fname in sys.argv[1:]:

    module = import_module(fname)
    recursive_selection(fname, module)

keys = list(container.keys())
keys.sort(key = str.lower)

for i in range(keys.__len__()):
    for j in range(i + 1, keys.__len__()):

        ratio = SequenceMatcher(None, container[keys[i]], container[keys[j]]).ratio()

        if ratio > 0.95:
            print(keys[i], keys[j])