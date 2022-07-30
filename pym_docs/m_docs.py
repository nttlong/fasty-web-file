from pym_docs.utils import wrapper_op
class BaseDocumentFields(object):
    """
    Ancestor of Mongodb parsable Field
    """

    def __init__(self, data=None, for_filter=False):
        self.__name__ = None
        self.__tree__ = None
        self.__for_filter__ = for_filter
        if isinstance(data, str):
            self.__name__ = data
        else:
            self.__tree__ = data

@wrapper_op()
class BsonDocumentObject(BaseDocumentFields):
    """
    Mongodb parable document field example:
    BsonDocumentObject().Amount*BsonDocumentObject().Price will be compile to {'$multiply': ['$Amount', '$Price']}
    """

    def __getattr__(self, item):
        if self.__fields__!=True:
            if item[0:2]!="__" or item[-2:]!="__":
                if self.__fields__.get(item,"") is None:
                    raise f"{type(self)}.{item} was not found"
        ret_field = None
        if self.__name__ != None:
            ret_field = BsonDocumentObject(self.__name__ + "." + item, self.__for_filter__)
            ret_field.__dict__.update({
                "__parent__": self,
                "__document__": self.__dict__.get("__document__", None)
            })

        else:
            ret_field = BsonDocumentObject(item, self.__for_filter__)
            ret_field.__dict__.update({
                "__parent__": self,
                "__document__": self.__dict__.get("__document__", None)
            })
        if self.__dict__.get("__type__", None) != None:
            # __type__ = self.__dict__.get("__type__").__origin__.__dict__.get(item).__origin__
            ret_field.__dict__.update({
                "__type__": self.__dict__.get("__type__").__origin__.__dict__.get(item)
            })

        return ret_field


    def __to_mongo_bson__(self):
        """
        parse to mongodb expression
        :return:
        """
        if self.__dict__.get("__alias__", None):
            if self.__tree__ == None:
                return {
                    self.__dict__["__alias__"]: self.__name__
                }
            elif self.__name__ == None:
                return {
                    self.__dict__["__alias__"]: self.__tree__
                }
            else:
                return {
                    self.__dict__["__alias__"]: {self.__name__: self.__tree__}
                }
        if self.__tree__ == None:
            return self.__name__
        return self.__tree__

    def to_bson(self):
        ret = self.__to_mongo_bson__()
        return ret

    def __repr__(self):
        ret = self.to_bson()
        if isinstance(ret, str):
            return ret
        elif isinstance(ret, dict):
            from bson import json_util
            import json
            return json.dumps(ret, default=json_util.default)

    def at(self,number:int):
        self.__index__=number
        if self.__tree__ is None:
            self.__name__=f"{self.__name__}.{number}"
            # self.__tree__=f"{self.__name__}[{number}]"
            return self
        return self
    def __call__(self, *args, **kwargs):
        print(args)
        print(kwargs)