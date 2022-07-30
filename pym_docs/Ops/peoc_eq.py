def proc_eq(a,b):
    from pym_docs.m_docs import BsonDocumentObject
    fa:BsonDocumentObject =a
    if fa.__tree__ is None:
        ret = BsonDocumentObject()
        ret.__is_simple__= True
        ret.__tree__ ={
            a.__name__:b
        }
        return ret