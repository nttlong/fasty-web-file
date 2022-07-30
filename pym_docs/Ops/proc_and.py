def proc_and(a,b):
    from pym_docs.m_docs import BsonDocumentObject
    fa: BsonDocumentObject = a
    fb: BsonDocumentObject = b
    if fa.__is_simple__ and fb.__is_simple__:
        ret= BsonDocumentObject()
        ret.__tree__={
            **fa.to_bson(),
            **fb.to_bson()
        }
        return ret
    else:
        ret = BsonDocumentObject()
        ret.__tree__ = {
            "$and":[
                fa.to_bson(),
                fb.to_bson()
            ]
        }
        return ret
    raise NotImplemented