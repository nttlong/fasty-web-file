import must_implement
from typing import List
class ItemInfo:
    pass
@must_implement.MustDeclare()
class Y:
    code1=(bool)
    messate_type=(str,True)
    items = List[ItemInfo]
    def __init__(self):
        self.code1=True
        self.messate_type="load data"
        self.items= []
        self.items.append(ItemInfo())

@must_implement.MustDeclare()
class X(Y):
    name:Y = (Y,True)
    def __init__(self):
        Y.__init__(self)
        self.messate_type="Load data lits"

x=X()
x.name=Y()

print(x.name)