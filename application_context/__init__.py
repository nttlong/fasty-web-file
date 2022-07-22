from fastapi import Request


class AppContext:
    def __init__(self, config: dict):
        self.default_db = config.get('db').get('authSource')
        self.db_name = self.default_db
        self.app_name = 'admin'

    def get_db_name(self,app_name) -> str:
        if app_name=='admin':
            return self.default_db
        return app_name


