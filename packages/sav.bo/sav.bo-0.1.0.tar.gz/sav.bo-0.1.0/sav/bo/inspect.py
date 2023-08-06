"""Module reflection for documentation and testing."""
from abc import ABCMeta, abstractmethod
from importlib import import_module
from inspect import getmembers, isclass, isfunction
from pathlib import Path
from types import FunctionType, ModuleType
from typing import Union, Any, Type, Optional, NamedTuple, List

from sav.bo.apriori import Initialized

DEFAULT_TESTS_UNQUAL = 'tests'  #: The default name for tests subpackages.


class Definitions(NamedTuple):
    """A structure of callables defined by a module."""

    functions: List[FunctionType]  #: List of function objects.
    classes: List[type]  #: List of class objects.
    exceptions: List[Type[Exception]]  #: List of exception classes.


class Inspectors(NamedTuple):
    """A structure of inspectors for submodules.

    ..  attribute: nonpack
        Inspectors for non-package modules.

        A sequence of instances of the appropriate subclass of
        :class:`ModuleInspector`.

    ..  attribute:
        Inspectors for subpackages.

        A sequence of instances of the appropriate subclass of
        :class:`PackageInspector`.

    """
    nonpack: List
    pack: List


ModuleRef = Union[ModuleType, str]


def get_module(ref: ModuleRef) -> ModuleType:
    return ref if isinstance(ref, ModuleType) else import_module(ref)


class ModuleInspector(Initialized):
    """Module inspection base class.

    :param module: The name or module object for the module to be
        inspected.
    :raises ImportError: If the module cannot be found.
    """

    def __init__(self, *, module: ModuleRef,
                 tests_unqual: str = DEFAULT_TESTS_UNQUAL,
                 **super_kwargs) -> None:
        super().__init__(**super_kwargs)
        self.tests_unqual = tests_unqual
        self.module: ModuleType = get_module(module)

    @property
    def name(self) -> str:
        """The dotted name of our module."""
        return self.module.__name__

    @property
    def is_test(self) -> bool:
        """Whether our module is a test module."""
        return self.tests_unqual in self.name.split('.')


class DefinitionsInspector(ModuleInspector, metaclass=ABCMeta):
    """ABC for inspection of function and class definitions.

    :param module: The name or module object for the module to be
        inspected.
    """

    def __init__(self, *, module: ModuleRef,
                 tests_unqual: str = DEFAULT_TESTS_UNQUAL,
                 **super_kwargs) -> None:
        super().__init__(module=module, tests_unqual=tests_unqual,
                         **super_kwargs)
        self._defs: Optional[Definitions] = None

    @abstractmethod
    def select_def(self, name: str) -> bool:
        """Whether to inspect the definition with the specified name."""
        pass

    def defines(self, obj: Any) -> bool:
        """Whether the specified object is defined in our module."""
        try:
            return obj.__module__ == self.name
        except AttributeError:
            return False

    @property
    def defs(self) -> Definitions:
        """A structure of callables defined in our module."""
        if self._defs is None:
            defs = Definitions([], [], [])
            for name, member in getmembers(self.module):
                if self.defines(member) and self.select_def(name):
                    members = (
                        (defs.exceptions if issubclass(member, Exception)
                         else defs.classes)
                        if isclass(member) else
                        (defs.functions if isfunction(member) else None)
                    )
                    if members is not None and (member.__name__ == name):
                        members.append(member)
            self._defs = defs
        return self._defs


class PackageInspector(ModuleInspector, metaclass=ABCMeta):
    """Inspect a whole tree of subpackages and modules.

    :param module: The name or module object for the package to be
        inspected.
    """

    def __init__(self, *, module: ModuleRef,
                 tests_unqual: str = DEFAULT_TESTS_UNQUAL,
                 **super_kwargs) -> None:
        super().__init__(module=module, tests_unqual=tests_unqual,
                         **super_kwargs)
        self._subs: Optional[Inspectors] = None

    def select_submodule(self, is_pack: bool, unqual: str) -> bool:
        """Whether to import the submodule with the specified name.

        :param is_pack: Whether the submodule is a package
        :param unqual: The unqualified submodule name.
        """
        return True

    @abstractmethod
    def create_subinspector(self, is_pack: bool, module: ModuleType) -> Any:
        """Should return a new inspector for the specified submodule."""
        pass

    @property
    def subs(self) -> Inspectors:
        """A structure of subpackages and submodules."""
        if self._subs is None:
            self._subs = Inspectors([], [])
            skip = {'__init__', '__pycache__'}
            for d in self.module.__path__:
                for p in Path(d).iterdir():
                    unqual = p.stem
                    if unqual in skip:
                        continue
                    if p.is_dir():
                        is_pack = True
                    elif p.suffix == '.py':
                        is_pack = False
                    else:
                        continue
                    skip.add(unqual)
                    if not self.select_submodule(is_pack, unqual):
                        continue
                    mod = import_module(self.name + '.' + unqual)
                    sub = self.create_subinspector(is_pack, mod)
                    self._subs[is_pack].append(sub)
        return self._subs
