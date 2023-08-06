"""Testing framework.

Organization of test modules and packages
=========================================

Tests are organized according to the following example::

    bo/
        foo/
            __init__.py
            bar.py
            baz.py
            tests/
                __init__.py
                bar.py
                baz.py
        tests/
             __init__.py

As the example shows, if there are tests for a package ``bo.foo``, then
these are placed in a companion package ``bo.foo.tests``. This package
is organized as a mirror of the target package. Hence, tests pertaining
to a module ``bo.foo.bar`` can be found in ``bo.foo.tests.bar``, except
in the case where ``.bar`` is itself a package, in which case its tests
will be located in ``bo.foo.bar.tests`` instead. Furthermore, tests for
the code in ``foo/__init__.py`` may be placed in ``foo/tests/__init__.py``.
"""
from itertools import chain
from types import ModuleType
from typing import Any
from unittest import TestLoader, TestSuite, TestCase

from sav.bo.cmd import ModuleRunner
from sav.bo.inspect import (ModuleInspector, PackageInspector, ModuleRef,
                            get_module, DEFAULT_TESTS_UNQUAL)
from sav.bo.terminals import FifoTerminalBackend, WorkDirTerminal


def create_test_backend(term=None, rel_path=None):
    wdterm = WorkDirTerminal(inner_term=term)
    test_root = wdterm.get_path('C:\\Users\\sander\\Test\\')
    if not test_root.exists():
        raise NotImplementedError
    fixture_root = test_root / 'temp'
    if rel_path:
        fixture_root = fixture_root / rel_path
    if not fixture_root.exists():
        fixture_root.mkdir(parents=True)
    wdterm.cwd = fixture_root
    return FifoTerminalBackend(inner_term=wdterm)


def load_tests_for(module: ModuleRef, loader: TestLoader, tests: TestSuite,
                   type_check: bool = False,
                   tests_unqual: str = DEFAULT_TESTS_UNQUAL) -> None:
    """Load tests for the specified module or package."""
    m = get_module(module)
    cls = PackageTester if hasattr(m, '__path__') else ModuleTester
    tester = cls(module=m, type_check=type_check, tests_unqual=tests_unqual)
    tester.load_tests(loader, tests)


class TypeChecker(TestCase):

    def __init__(self, tester: 'ModuleTester') -> None:
        super().__init__()

        # Avoid possible mixup with TestCase implementation
        self.__tester = tester

    def runTest(self) -> None:
        flag = '-p' if isinstance(self.__tester, PackageTester) else '-m'
        completed = ModuleRunner().run('mypy', flag, self.__tester.name)
        self.assertEquals(completed.returncode, 0)


class ModuleTester(ModuleInspector):
    """Module inspector that can load tests into a test suite."""

    def __init__(self, *,
                 module: ModuleRef,
                 type_check: bool = False,
                 tests_unqual: str = DEFAULT_TESTS_UNQUAL,
                 **super_kwargs) -> None:
        super().__init__(module=module, tests_unqual=tests_unqual,
                         **super_kwargs)
        self.type_check = type_check

    def load_tests(self, loader: TestLoader, tests: TestSuite) -> None:
        """Load tests for our module into the specified test suite.

        If our module is a test module or package, we load tests from it.

        If our module is a package but not a test package, then all
        tests will be located in its subpackages. This method will
        do nothing and return control to :meth:`PackageTester.load_tests`,
        which will proceed to traverse into those subpackages.

        If our module is neither a package nor a test module, then
        this :class:`ModuleTester` has not been constructed by a
        parent :class:`PackageTester`, which would only have traversed
        into subpackages. Therefore, whoever constructed this
        :class:`ModuleTester` must have wanted to load tests for our
        module specifically, and know that an associated test module exists.
        This module will be imported, and tests will be loaded from it.

        :raises ImportError: If the test module for this module could not
            be found.
        """
        if self.type_check:
            tests.addTest(TypeChecker(tester=self))
        if self.is_test:
            tests.addTests(loader.loadTestsFromModule(self.module))
        elif not isinstance(self, PackageTester):
            s = self.name.split('.')
            s.insert(-1, self.tests_unqual)
            tester = ModuleTester(module='.'.join(s),
                                  tests_unqual=self.tests_unqual)
            tester.load_tests(loader, tests)


class PackageTester(ModuleTester, PackageInspector):
    """Recursive test loader for packages and submodules."""

    def select_submodule(self, is_pack: bool, unqual: str) -> bool:
        """Select which submodules to inspect for test collection.

        If our package is a test package, select all submodules.
        Otherwise, only select subpackages.

        Implements :meth:`bo.inspect.PackageInspector.select_submodule`
        """
        return is_pack or self.is_test

    def create_subinspector(self, is_pack: bool, module: ModuleType) -> Any:
        """Create package or module tester.

        Implements
        :meth:`bo.inspect.PackageInspector.create_subinspector`
        """
        cls = (PackageTester if is_pack else ModuleTester)
        return cls(module=module, tests_unqual=self.tests_unqual)

    def load_tests(self, loader: TestLoader, tests: TestSuite) -> None:
        """Load all tests for our package and its submodules."""
        super().load_tests(loader, tests)
        for sub in chain.from_iterable(self.subs):
            sub.load_tests(loader, tests)
