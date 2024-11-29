from PySide6.QtCore import QObject

class UserData(QObject):
    def __init__(self):
        super().__init__()
        self.jwt_token = None
        self.graph_data = None

    def set_jwt_token(self, token):
        self.jwt_token = token

    def get_jwt_token(self):
        return self.jwt_token
    
    def set_graph_data(self, data):
        self.graph_data = data
    
    def get_graph_data(self):
        return self.graph_data

    def delete_graph_data(self):
        self.graph_data = None

