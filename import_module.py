from pycalc.parse_epression import list_module, operators, static_value, list_functions


def imp_module():
    """
    Module import function
    """
    for modname in list_module:
        try:
            modules = __import__(modname)
            for key in modules.__dict__:
                if callable(modules.__dict__[key]):
                    operators[key] = (7, getattr(modules, key))
                    list_functions.append(key)
                else:
                    static_value[key] = getattr(modules, key)
        except ImportError:
            raise ImportError("Module {} not found:".format(modname))
