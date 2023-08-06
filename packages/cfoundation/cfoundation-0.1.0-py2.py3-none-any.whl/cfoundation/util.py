import inspect
import sys
import re
from pydash import _
from os import path

_app = None

def get_app():
    global _app
    return _app

def register(app):
    global _app
    stack = inspect.stack()
    root_path = get_root_path(stack)
    services = get_services(root_path)
    controllers = get_controllers(root_path)
    setattr(app, 'services', services)
    setattr(app, 'controllers', controllers)
    _app = app
    register_services(app.services)
    register_controllers(app.controllers)

def get_services(root_path):
    services = Services()
    module = dynamic_import('services', path.join(root_path, 'services', '__init__.py'))
    for key in _.keys(module):
        matches = re.findall(r'[A-Z].*Service', key)
        if len(matches) > 0:
            setattr(services, _.snake_case(key), getattr(module, key)())
    return services

def get_controllers(root_path):
    controllers = Controllers()
    module = dynamic_import('controllers', path.join(root_path, 'controllers', '__init__.py'))
    for key in _.keys(module):
        matches = re.findall(r'[A-Z].*Controller', key)
        if len(matches) > 0:
            setattr(controllers, _.snake_case(key), getattr(module, key)())
    return controllers

def register_services(services):
    for key in _.keys(services):
        getattr(services, key).register()

def register_controllers(controllers):
    for key in _.keys(controllers):
        getattr(controllers, key).register()

def get_root_path(stack):
    caller_path = stack[1][1]
    return path.abspath(path.dirname(caller_path))

def dynamic_import(name, path=None):
    if not path:
        return __import__(name, globals(), locals(), [], 0)
    elif sys.version_info > (3, 0):
        importlib = __import__('importlib', globals(), locals(), [], 0)
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    elif sys.version_info > (3, 0):
        importlib = __import__('importlib', globals(), locals(), [], 0)
        from importlib.machinery import SourceFileLoader
        return SourceFileLoader(name, path).load_module()
    else:
        imp = __import__('imp', globals(), locals(), [], 0)
        return imp.load_source(name, path)

class Services():
    pass

class Controllers():
    pass
