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
    singleton1 = Template(fields)
    singleton2 = Template({"username": "Daisy", "email": "daisy"})
    singleton1.print_dict()
    singleton2.print_dict()


test_singleton({"username": {"Filoenna": str, str: "email", int: "machefi2"}})
