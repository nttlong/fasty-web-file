from must_implement import MustImplement

class BaseMessage:
    def send_dict_data(self,group_id:str,data:dict):
        raise NotImplemented

    def append_binary_content_to_temp(self, app_name, relative_path, b_data):
        raise NotImplemented

    def get_content_location(self, app_name, relative_path):
        raise NotImplemented


@MustImplement()
class FakeMessage(BaseMessage):
    def send_dict_data(self,group_id:str,data:dict):
        pass
    def append_binary_content_to_temp(self, app_name, relative_path, b_data):
        pass
    def get_content_location(self, app_name, relative_path):
        pass
