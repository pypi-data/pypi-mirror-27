from abc import ABCMeta
from unittest import TestCase

from sav.bo.apriori import SingletonMeta, SingletonABCMeta, Initialized


class _NonSingletonFoo:
    pass


class _SingletonFoo(metaclass=SingletonMeta):
    pass


class _AbstractBar(metaclass=ABCMeta):
    pass


class _NonSingletonBar(_AbstractBar):
    pass


class _SingletonBar(_AbstractBar, metaclass=SingletonABCMeta):
    pass


class TestSingletons(TestCase):
    def test_singleton_meta(self):
        a = _NonSingletonFoo()
        b = _NonSingletonFoo()
        c = _SingletonFoo()
        d = _SingletonFoo()
        self.assertNotEqual(a, b)
        self.assertEqual(c, d)

    def test_singleton_abc_meta(self):
        a = _NonSingletonBar()
        b = _NonSingletonBar()
        c = _SingletonBar()
        d = _SingletonBar()
        self.assertNotEqual(a, b)
        self.assertEqual(c, d)


class _A(Initialized):
    pass


class _B(_A):
    pass


class _C(_A):
    def __init__(self, *, c_a, **super_kwargs):
        self.a = c_a
        super().__init__(**super_kwargs)


class _D(_B, _C):
    pass


class TestInitialized(TestCase):

    def test_buck_stopper(self):
        x, y = range(2)
        with self.assertRaises(TypeError) as cm:
            some_d = _D(c_a=x)
            _D(c_a=x, unknown_arg=y)
        self.assertEqual(some_d.a, x)
        s, t = str(cm.exception), str({'unknown_arg': y})
        self.assertEqual(s[-len(t):], t)
