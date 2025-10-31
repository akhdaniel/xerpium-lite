class BaseUISchema:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def get_ui_schema(self):
        raise NotImplementedError
