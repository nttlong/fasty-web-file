from pym_docs import bson_doc_from_type
class User:

    Name = None
    Code = str
ffx=dict(
    XX=1
)
doc_user =bson_doc_from_type(User)

fx=("123456"==doc_user.Code) | (doc_user.Name=="YYYY")
print(fx)
fx=doc_user.Code=="yyy"
print(fx)