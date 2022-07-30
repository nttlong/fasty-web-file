from must_implement import MustImplement

class BaseMessage:
    def send_dict_data(self,group_id:str,data:dict):
        raise NotImplemented



@MustImplement()
class FakeMessage(BaseMessage):
    def send_dict_data(self,group_id:str,data:dict):
        pass

