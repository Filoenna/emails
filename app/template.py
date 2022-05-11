class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Template(metaclass=SingletonMeta):
    def __init__(self, fields):
        self.fields = fields

    def print_dict(self):
        for k, v in self.fields.items():
            print(f"{k}: {v}")


def test_singleton(fields):
    singleton = Template(fields)
    singleton.print_dict()


test_singleton({"username": "Filoenna", "email": "machefi2"})
