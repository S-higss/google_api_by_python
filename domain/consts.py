class ConstantMeta(type):
    """A metaclass for classes that manage constants.
    Prevents class variables from being overwritten or new class variables from being added.
    """

    # A variable indicating whether the class has been initialized.
    _initialized = False

    def __setattr__(cls, name, value):
        if cls._initialized:
            if name in cls.__dict__:
                raise ValueError(f"{name} is a read-only property")
            else:
                raise AttributeError("Cannot add new attribute to Constants class")
        super().__setattr__(name, value)

    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls._initialized = True


# A class for managing constants
class SystemConstants(metaclass=ConstantMeta):
    config = "config.toml"
    encode = "utf-8"