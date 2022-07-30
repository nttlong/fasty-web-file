def proc_or(a,b):
    from pym_docs.m_docs import BsonDocumentObject
    fa: BsonDocumentObject = a
    fb: BsonDocumentObject = b
    ret = BsonDocumentObject()
    ret.__tree__ = {
        "$or": [
            fa.to_bson(),
            fb.to_bson()
        ]
    }
    return ret