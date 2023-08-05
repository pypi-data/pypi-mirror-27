class Singleton(object):
    _instance = None
    _initialized = False

    def __new__(cls, *args):
        if cls._instance == None:
            cls._instance = object.__new__(cls)
        cls.__init__()
        return cls._instance

    def __init__(self, a):
        if not self.__class__._initialized:
            self.arg = a
            self.__class__._initialized = True



class ClassName(object):
    """docstring for ."""
    def __init__(self, arg):
        super(ClassName, self).__init__()
        self.arg = arg

a = ClassName(1)
print(a)
