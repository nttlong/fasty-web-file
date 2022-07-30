from typing import TypeVar, Generic
T = TypeVar('T')


def bson_doc_from_type(doc_type:T)->T:
    from pym_docs.m_docs import BsonDocumentObject
    from pym_docs.field_types import FieldType
    if(hasattr(doc_type,"__dict__")):
        fields=[x for x in doc_type.__dict__.keys() if  x[0:2]!="__" or x[-2:]!="__" ]
        dict_fields={}
        for x in fields:
            declareation = getattr(doc_type,x)
            dict_fields[x]= FieldType(x,declareation)

        ret= BsonDocumentObject()
        setattr(ret,"__fields__",dict_fields)
    else:
        ret = BsonDocumentObject()
        setattr(ret, "__fields__", True)
    return ret



