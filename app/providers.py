class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Providers(metaclass=SingletonMeta):
    def __init__(self, fields):
        self.fields = fields

    def print_dict(self):
        for k, v in self.fields.items():
            print(f"{k}: {v}")

    def __getitem__(self, key):
        for k, v in self.fields.items():
            if k == key:
                return v
