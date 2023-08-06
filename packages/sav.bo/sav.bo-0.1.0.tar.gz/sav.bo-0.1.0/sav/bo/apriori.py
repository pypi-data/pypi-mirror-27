"""First module of the Bo library to be loaded.

This module contains core functions and classes which help implement
coding techniques and conventions used throughout the package.


Argument-passing to upstream methods
====================================

Object-oriented programming typically involves two design patterns
where the method of an object may invoke what we might call an
"upstream" version of itself. The first such pattern is the decorator
pattern (not to be confused with Python decorators) which involves
an object ``x`` wrapping around an object ``x.y`` such that an outer
method ``x.foo()`` will invoke an inner method ``self.y.foo()``. The
second pattern is that of inheritance, where a method ``x.foo()``,
belonging to some class of which ``x`` is an instance, will invoke
an overridden method ``super().foo()`` belonging to the next class
in the method resolution order (MRO). In both cases, the upstream
method performs some basic functionality which is modified or expanded
upon by the downstream method.


Common vs. unique arguments
---------------------------

When we consider the relation between such upstream and downstream
methods, we should distinguish between two types of arguments. The
first is the type of argument that needs to be processed by each of
the methods. Suppose that ``Logger`` is a class with an abstract method
``log(message)``, which is implemented in different ways by
``DisplayLogger`` and ``FileLogger``. Suppose furthermore that you want
``DisplayFileLogger`` to inherit from both, such that each message is
displayed as well as written to a file. In that case, the
``DisplayLogger.log`` method needs to both process and pass on the
message argument. Let us call such arguments "common arguments".

By contrast, we encounter the second type of argument when
different arguments need to be processed by the different versions
of the method. For example, in addition to the common ``message``
argument, the ``DisplayLogger.log`` method might accept a ``color``
argument, while the ``FileLogger.log`` method might accept a ``file``
argument (it would be better to implement such functionality in a
different way but this is just for the sake of the example). In that
case, the ``DisplayLogger.log`` should also accept both the ``color``
and the ``file`` arguments, because it needs to pass the ``file``
argument on to the ``FileLogger.log`` method. Let us call these
"unique arguments".

Note that we can make the same distinction between the common
``message`` argument and the unique ``color`` and ``file`` arguments
if we would implement ``DisplayLogger`` and ``FileLogger`` as wrapper
classes according to the decorator pattern. Some implementations of
the decorator pattern may simply rule out they very idea of
unique arguments, such that all methods strictly conform to the same
signature, but in many cases this would impose an undesirable
limitation on the design of our classes.


The buck-passing paradigm
-------------------------

It is often considered more Pythonic to pass arguments explicitly,
whenever possible, rather than curling them up in variable length
parameters. In the case of common arguments, this is usually not a
problem, because every method knows about all of them. Furthermore,
it is okay to pass common arguments as positional arguments, because
every method knows in what order to expect them. In the case of
unique arguments, however, this is only possible when the upstream
classes are fixed. This is true in the case of single inheritance,
but not in the case of cooperative multiple inheritance. Furthermore,
it may be true for implementations of the decorator pattern which
impose a strict wrapping order, such that a ``DisplayLogger`` should
always be wrapped around a ``FileLogger`` rather than vice-versa,
but such regimentation would greatly reduce the dynamic flexibility
of the decorator pattern. It seems desirable, then, that we can
wrap a ``FileLogger`` around a ``DisplayLogger`` and still pass
a unique ``color`` argument to the ``FileLogger``'s ``log`` method
even though it knows nothing about colors, and simply expect it
to pass that argument on to the ``DisplayLogger``.

The "buck-passing" paradigm, used throughout the :mod:`caryatid` package,
addresses this type of situation. It makes use of keyword-only
arguments, such that each method removes its own keyword parameters
from the passed arguments, passing on any unknown keyword arguments
by means of a variable-length keyword parameter (named
``**super_kwargs`` in the case of inheritance, or ``**inner_kwargs``
in the case of the decorator pattern).
Finally, the innermost method must know that it is the innermost
method. In the case of the decorator pattern this is typically true
because there is always an innermost object which must belong to a
class that does not require being wrapped around another object to
pass arguments on to. In the case of multiple inheritance, this is
achieved by defining a common base class for all potential siblings.

The variable-length keyword parameter represents the "buck" of
unrecognized unique arguments. While all the other methods are allowed
to pass the buck, the final method must stop it. This is done by
checking whether the remaining ``unexpected_kwargs`` argument evaluates to
``True``. If it does, meaning that it is non-empty, then a
:exc:`TypeError` should be raised. For convenience, this functionality
is provided by the :func:`check_unexpected_kwargs` function.

Example::

    class Logger:
        def log(message, **unexpected_kwargs):
            check_unexpected_kwargs(unexpected_kwargs)

    class DisplayLogger(Logger):
        def log(message, *, color, **super_kwargs):
            super().log(message, **super_kwargs)
            ... # display message in color

    class FileLogger(Logger):
        def log(message, *, file, **super_kwargs):
            super().log(message, **super_kwargs)
            ... # write message to file

    class DisplayFileLogger(DisplayLogger, FileLogger):
        pass

Note how the methods in this example also employ the ``*``
parameter to ensure that recognized unqique parameters are
keyword-only. It is advised to always do this, because mistakes
are easily made when unique arguments are passed as positional
arguments in dynamic environments.


Buck-passing and object initialization
--------------------------------------

A common real-life example of unique arguments in the case of
cooperative inheritance involves the ``__init__`` methods of
sibling classes. Typically, the different ``__init__`` methods in the
method resolution order have different call signatures because they
initialize different member variables. And since the next class in the
MRO is not always the same, the downstream ``__init__`` method must be
able to invoke different upstream methods that require different
arguments.

The problem with ``__init__`` methods is of course that so may classes
define these methods, that it becomes a challenge, whenever you want
to inherit from two classes ``X`` and ``Y``, to make sure that ``X``
and ``Y`` in turn both inherit from a common base class that is
properly cooperative. That is why this module defines a
designated base class :class:`Initialized`, which defines an
``__init__`` method that will stop the buck.

Typically, any class in this package which defines an ``__init__``
method and which might have to support cooperative inheritance should
be a subclass of :class:`Initialized` and make sure that the
``__init__`` method conforms to the buck passing paradigm. Hence, each
such method should include the ``**super_kwargs`` argument and pass it on
to ``super().__init__()``, as in the following example::

    class Foo(Initialized):
        def __init__(*, fookey, **super_kwargs):
            super().__init__(**super_kwargs)
            self.foovar = fookey


Keeping the chain between cooperative siblings intact
-----------------------------------------------------

There is another reason why it is advised to define a
common base class for cooperative siblings, which is that it prevents
the chain between the siblings from being broken by an overridden
method in a superclass that is not part of the cooperative framework.
For example, suppose that ``A`` and ``B`` both implement a method
``foo()`` cooperatively, and that ``AB`` inherits from ``A`` and ``B``
in that order. Suppose furthermore that ``A`` also inherits from a
third-party class ``T`` which also defines ``foo()``, such that
``A.foo()`` overrides ``T.foo()``, but that ``A.foo()`` does not need
to call ``T.foo()`` (the latter might be an empty abstract method,
for example, which is invoked by other methods of ``T``, methods
which you want ``A`` to inherit). The problem is that when ``T`` is
not a superclass of ``B``, the call to ``super.foo()`` in ``A`` might
go to ``T.foo()`` instead of ``B.foo()``, because ``T`` might precede
``B`` in the method resolution order (MRO) for ``AB``. This is easily
solved by defining a common base class ``C`` for ``A`` and ``B``,
where ``C`` precedes ``T`` in the list of base classes for ``A``.
This will cause ``B`` to precede ``T`` in the MRO for ``AB``.

Note that the situation is different when ``A.foo()`` does need to
invoke ``T.foo()``. In that case, using cooperative multiple inheritance
to derive ``AB`` from both ``A`` and ``B`` might not be the best
solution, and you should consider alternative approaches.
"""
from abc import ABCMeta, abstractmethod
from typing import TypeVar, Any, GenericMeta, Mapping, Callable, Optional, Dict


T = TypeVar('T')


class SingletonMeta(type):
    """Singleton metaclass.

    Specify this class as the metaclass of your user defined class in
    order to turn it into a singleton class. If ``Foo`` is a singleton
    class, then every call to ``Foo()`` will return the same instance
    of ``Foo``. The instance is created the first time that ``Foo()``
    is invoked.

    This metaclass expects that no arguments will be
    passed to the singleton constructor, since that would allow
    different constructor calls with different arguments to be made.
    If arguments are passed to a singleton constructor, this metaclass
    will intercept them and raise a :exc:`TypeError`. Thus, no
    constructor arguments are ever passed on to the ``__new__`` method
    of the singleton class.

    If the construction of the singleton instance of ``Foo`` requires
    certain arguments to be passed to the ``__new__`` method of the
    superclass of ``Foo``, then ``Foo`` should define a ``__new__``
    method which receives no arguments but which does pass the
    required values to the ``__new__`` method of its superclass.

    You should only define a singleton class in the following scenario:

    - You need something that is completely immutable and global.
    - You need it to also be of a more generic type of which
      there are other instances.
    """

    _instances: Dict[type, Any] = {}

    def __call__(cls, *args, **kwargs) -> Any:
        if args or kwargs:
            raise TypeError('Arguments were passed to singleton constructor.')
        try:
            instance = cls._instances[cls]
        except KeyError:
            instance = super().__call__()
            cls._instances[cls] = instance
        return instance


class SingletonABCMeta(SingletonMeta, ABCMeta):
    """Metaclass for singleton implementations of ABCs."""
    pass


class SingletonGenericMeta(SingletonABCMeta, GenericMeta):
    """Metaclass for singleton implementations of generic classes."""
    pass


def find_super(obj: Any, cls: type, name: str) -> Optional[type]:
    """Search for next class in the MRO that defines some attribute.

    :param obj: The object whose MRO should be searched.
    :param cls: Only classes that succeed this class in the MRO
        will be searched.
    :param name: The name of the attribute to look for.
    :return: The first successor class in the MRO to define the
        specified attribute, or `None` if none could be found.
    """
    mro = obj.__class__.__mro__
    for c in mro[mro.index(cls) + 1:]:
        # Check class dict
        # This excludes inherited attributes
        if name in c.__dict__:
            return c
    return None


def check_unexpected_super(obj: Any, cls: type, name: str) -> None:
    """Check that a method is not defined higher up in the MRO.

    If the method is defined only by :class:`object` then this method
    also returns without raising an error.

    :raise TypeError: if ``name`` is defined by a class that appears
        somewhere between ``cls`` and :class:`object` in the method
        resolution order of ``obj``.
    """

    cls = find_super(obj, cls, name)
    if (cls is None) or (cls is object):
        return
    s = 'Unexpected super method: {}.{}.{}'
    s = s.format(cls.__module__, cls.__qualname__, name)
    raise TypeError(s)


def check_unexpected_kwargs(kwargs: Mapping[str, Any]) -> None:
    """Checks whether unexpected unique arguments were received."""
    if kwargs:
        raise TypeError('Unexpected keyword arguments: {}'.format(kwargs))


class Initialized:
    """Base class that provides a buck stopper ``__init__`` method.

    :param unexpected_kwargs: unique arguments passed on by downstream
        ``__init__`` methods
    :raises TypeError: if ``unprocessed`` is non-empty, or if any
        class preceding this class in the MRO of the instance defines
        an __init__ method (other than :class:`object`).

    This class may be used as the common ancestor for classes that
    implement cooperative multiple inheritance of the ``__init__``
    method.

    Note that this class does not call any implementations of the
    ``__init__`` method further up in the MRO, but instead raises
    an exception when the next ``__init__`` method in the MRO is
    not ``object.__init__``. Thus, you should make sure that any other
    classes that follow ``Initialized`` in the MRO of your classes are
    effectively mixins that do not override ``object.__init__``.
    """

    def __init__(self, **unexpected_kwargs) -> None:
        check_unexpected_super(self, Initialized, '__init__')
        check_unexpected_kwargs(unexpected_kwargs)


def lazy_default(passed: Any, func: Callable[..., Any], *args,
                 **kwargs) -> Any:
    """Return a specified value or evaluate a default expression.

    Consider the following statements::

        self.foo = Foo() if foo is None else foo
        return (Bar(x=3, y=5) if self.bar is None else self.bar)

    In both cases, an expression is evaluated which is a logical
    function of what we might call the primary expression ``E`` and
    the default expression ``D``. The latter is evaluated if the
    former evaluates to ``None``. The compound expression has the
    following form::

        D if E is None else E

    There are two problems with this expression. The first is that
    we have to mention E twice. When E is a long variable name, this
    will make the line unneccesarily long. Furthermore, if E is an
    expression instead of a variable, it will be evaluated twice! To
    avoid this, we might have to evaluate the value of E and assign
    it to a temporary variable first, which is also not elegant.
    The second problem is that it is so common to use None as the
    value for E that triggers the evaluation of D that it would be
    nice if we could omit it. Instead of the format above, it would
    be nice if Python would allow the following expression::

        default(E, D)

    Note, however, that this would require `default` to be a special
    language construct, because if it were a regular function, Python
    would have to evaluate ``D`` every time the function were called,
    instead of only in those cases where ``E`` turned to be ``None``.
    To make it work with a regular function, the second argument must
    not be a value, but a factory function. This allows for two easy
    usage patterns. The first is to use a ``lambda`` expression::

        lazy_default(E, lambda: D)

    The second is to pass a callable name and, optionally, any
    positional or keyword arguments to call it with::

        # calls Foo() if foo is None
        self.foo = lazy_default(foo, Foo)

        # calls Bar(x=3, y=5) if self.bar is None
        return lazy_default(self.bar, Bar, x=3, y=5)

    :param passed: The value to be passed through unless it is ``None``.
    :param func: The function to call if a default value is needed.
    :param args: Any positional arguments to pass to the default function.
    :param kwargs: Any keyword arguments to pass to the default function.
    :return: The specified or the default value.
    """
    return func(*args, **kwargs) if passed is None else passed


class Cache(Initialized, metaclass=ABCMeta):
    def __init__(self, **super_kwargs) -> None:
        super().__init__(**super_kwargs)
        self.outdated: bool = True

    @abstractmethod
    def update(self) -> None:
        pass

    def refresh(self) -> None:
        self.update()
        self.outdated = False

    def check(self) -> None:
        if self.outdated:
            self.refresh()
