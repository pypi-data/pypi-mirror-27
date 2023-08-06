class cached_property:
    """参见: django.utils.functional.cached_property
    """

    def __init__(self, func, name=None):
        self.func = func
        self.__doc__ = getattr(func, '__doc__')
        self.name = name or func.__name__

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        res = instance.__dict__[self.name] = self.func(instance)
        return res


class InstanceMeta(type):
    """类的自动实例化

    用法:

        class MyClass(metaclass=InstanceMeta):
            pass

    相当于:

        class MyClass(metaclass=InstanceMeta):
            pass

        MyClass = MyClass()

    abstract 的用法（指定了 abstract=True 的类不会被实例化，可以用作基类）:

        class MyBase(metaclass=InstanceMeta, abstract=True):
            pass

        class MyClass1(MyBase):
            pass

        class MyClass2(MyBase):
            pass
    """

    def __new__(mcs, name, bases, namespace, abstract=False):
        cls = super().__new__(mcs, name, bases, namespace)

        if abstract:
            return cls

        return cls()


class Instance(metaclass=InstanceMeta, abstract=True):
    """用继承的方法实现类的实例化

    用法：

        class MyClass(Instance):
            pass

    相当于：

        class MyClass(Instance):
            pass

        MyClass = MyClass()
    """
