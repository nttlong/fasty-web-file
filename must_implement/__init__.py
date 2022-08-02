import sys
from typing import List, TypeVar

T = TypeVar("T")

def MustImplement():
    """
    Dùng để kiểm tra tính toàn vẹn 1 class và impletementation of class khác
    :return:
    """

    def wrapper(*x, **y):
        __cls__ = x[0]
        __cls__module_path__ = str(sys.modules[__cls__.__module__])
        __base__ = __cls__.__base__
        for k, v in __base__.__dict__.items():
            if (k[0:2] != "__" and k[:-2] != "__") :
                if callable(v):
                    if __cls__.__dict__.get(k) is None:
                        raise Exception(
                            f"{__cls__.__module__}.{__cls__.__name__}.{k} was not implement in'{__cls__module_path__}' ")

                    v2 = __cls__.__dict__.get(k)
                    if v.__code__.co_argcount != v2.__code__.co_argcount:
                        args = []
                        args2 = []
                        for i in range(0, v.__code__.co_argcount):
                            args += [v.__code__.co_varnames[i]]
                            if i < v2.__code__.co_argcount:
                                args2 += [v2.__code__.co_varnames[i]]

                        raise Exception(

                            f"'{v2.__code__.co_filename}', line {v2.__code__.co_firstlineno}\n"
                            f"see:\n"
                            f"'{v.__code__.co_filename}', line {v.__code__.co_firstlineno} \n"
                            f"\n"
                            f"{__cls__.__module__}.{__cls__.__name__}.{k}({str.join(',', args2)}) but {__base__.__module__}.{__base__.__name__}.{k}({str.join(',', args)})\n "
                            f"")

        return __cls__

    return wrapper

class __property__:
    def __init__(self,settings):
        if not isinstance(settings,tuple):
            settings=[settings]
        else:
            settings = list(settings)
        self.is_required=False
        self.check_data_types = settings
        check_is_require = settings[-1:][0]
        if check_is_require ==True or settings[-1:][0]==False:
            if settings.__len__()<2:
                self.error=True
        if type(self.is_required)!=bool:
            self.is_required=False
        self.is_required =check_is_require
        self.check_data_types=settings[0]

    def check_value(self,value):
        if value is None and self.is_required==True:
            return 1
        elif value is None:
            return 0
        if isinstance(self.check_data_types,list):
            if not type(value) in self.check_data_types:
                return 2
        elif hasattr(self.check_data_types,"__origin__") and self.check_data_types.__origin__==type(value):
            return 0
        elif type(value) != self.check_data_types:
            return 2
        return 0

    def get_types(self):

        if isinstance(self.check_data_types, list):
            return ",".join(self.check_data_types)
        else:
            return self.check_data_types


def __must_declare__getitem__(owner,item):
    pass
__FIELD_NAMES_KEY__= "__field_names__"
__FIELD_SETTINGS_KEY__= "__field_settings__"
__FIELD_DATA_KEY___= "__field_data__"
def MustDeclare():
    def wrapper(*args,**kwargs):
        cls_type = args[0]

        b=cls_type
        fields = []
        while b!=object:
            fields =list(set(fields).union(set([(x,b.__dict__.get(x)) for x in b.__dict__.keys() if x[0:2]!="__" or x[-2:]!="__"])))
            b = b.__base__


        fields_dict={}
        for x in fields:
            property_setting = __property__(x[1])
            fields_dict[x[0]]=property_setting
        setattr(cls_type, __FIELD_NAMES_KEY__, fields)
        setattr(cls_type, __FIELD_SETTINGS_KEY__, fields_dict)
        old___getattribute__ = None
        old___setattr__ = getattr(cls_type, "__setattr__")
        old___getattribute__ = getattr(cls_type, "__getattribute__")
        def new_getattr(owner,item):
            global __FIELD_NAMES_KEY__
            global __FIELD_SETTINGS_KEY__
            global __FIELD_DATA_KEY___
            if item[0:2]=="__" and item[-2:]=="__":
                return old___getattribute__(owner, item)
            else:
                t= type(owner)
                if not hasattr(t, __FIELD_SETTINGS_KEY__):
                    raise Exception(f"{item} was not declare in {t}\n{t.__code__}")

                check_dict = getattr(t, __FIELD_SETTINGS_KEY__)
                if not isinstance(check_dict,dict):
                    raise Exception(f"{item} was not declare in {t}\n{t.__code__}")
                elif check_dict.get(item) is None:
                    source_file = sys.modules[t.__module__].__file__
                    raise Exception(f"'{t.__name__}.{item}' was not declare in {t}\n{source_file}")
                data:dict = old___getattribute__(owner, "__dict__")
                if data.get(__FIELD_DATA_KEY___) is None:
                    data[__FIELD_DATA_KEY___]={}
                return data[__FIELD_DATA_KEY___].get(item)
        def new_setattr(owner,item,value):
            if item[0:2]=="__" and item[-2:]=="__":
                return old___setattr__(owner, item,value)
            t = type(owner)
            if not hasattr(t, __FIELD_SETTINGS_KEY__):
                raise Exception(f"{item} was not declare in {t}\n{t.__code__}")

            check_dict = getattr(t, __FIELD_SETTINGS_KEY__)
            if not isinstance(check_dict, dict):
                raise Exception(f"{item} was not declare in {t}\n{t.__code__}")
            check_value:__property__ = check_dict.get(item)
            if check_value is None:
                source_file = sys.modules[t.__module__].__file__
                raise Exception(f"'{t.__name__}.{item}' was not declare in {t}\n{source_file}")
            check_result = check_value.check_value(value)
            if check_result!=0:
                source_file = sys.modules[t.__module__].__file__
                if check_result== 1:
                    raise Exception(f"Invalid data type when set '{t.__name__}.{item}' \n"
                                    f"'{t.__name__}.{item}' must be not None,\n"
                                    f"see:'{source_file}'")

                if check_result==2:
                    raise Exception(f"Invalid data type when set '{t.__name__}.{item}' \n"
                                    f"'{t.__name__}.{item}' must be {check_value.get_types()}\n"
                                    f"Please preview {t}\n{source_file}")
            data: dict = old___getattribute__(owner, "__dict__")
            if data.get(__FIELD_DATA_KEY___) is None:
                data[__FIELD_DATA_KEY___] = {}
            data[__FIELD_DATA_KEY___][item]=value

        setattr(cls_type,"__getattribute__",new_getattr)
        setattr(cls_type,"__setattr__",new_setattr)

        return cls_type
    return wrapper

def new_instance(cls_type:T,data:dict)->T:
    if not hasattr(cls_type, __FIELD_NAMES_KEY__) and not hasattr(cls_type, __FIELD_SETTINGS_KEY__):
        cls_type = MustDeclare()(cls_type)
    cls_settings = getattr(cls_type,__FIELD_SETTINGS_KEY__)
    cks_keys = cls_settings.keys()

    data_keys = [x for x in data.keys() if x[0:2]!="__" or x[-2:]!="__"]
    keys=list(set(cks_keys).union(data_keys))

    ret = cls_type()
    for key in data_keys:
        setattr(ret,key,data.get(key,None))
    return ret

def get_dict(instance)->dict:
    cls_type=type(instance)

    if not hasattr(cls_type, __FIELD_NAMES_KEY__) and not hasattr(cls_type, __FIELD_SETTINGS_KEY__):
        raise Exception("Invalid data type")
    cls_settings = getattr(cls_type,__FIELD_SETTINGS_KEY__)
    cks_keys = cls_settings.keys()
    ret ={}
    for k in cks_keys:
        ret[k]=getattr(instance,k)
    return ret
