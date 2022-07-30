class __test__:
    pass

__list_of_ops__=[
    "eq",
    "and",
    "or"
]

def wrapper_op():
    def wrapper(*args,**kwargs):
        t=args[0]
        import pym_docs.Ops
        import sys
        mdl = sys.modules[pym_docs.Ops.__name__]
        global __list_of_ops__
        for x in __list_of_ops__:
            proc_name = f"proc_{x}"
            if not hasattr(mdl,proc_name):
                raise Exception(f"{proc_name} was not founfd in {mdl.__file__}")
            fn = getattr(mdl, proc_name)

            setattr(t, f"__{x}__", fn)
        return t
    return wrapper
