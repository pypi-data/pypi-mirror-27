"""Abstraction layer for commands that accept string arguments.

This module provides a generalized interface for the invocation of
programs, modules, terminal commands, or any other text-based calling
protocol. Its format is loosely based on that of the :mod:`subprocess`
module, but it does not import it.

The interface is extended further by the :mod:`sav.bo.terminals`
module, which provides a number of wrapper classes that may be used
to implement a decorator pattern on top of the :mod:`subprocess` module.
"""
import sys
from abc import abstractmethod, ABCMeta
from contextlib import (ExitStack, redirect_stdout, redirect_stderr,
                        contextmanager)
from enum import Enum
from runpy import run_module
from typing import Any, Sequence

from sav.bo.apriori import SingletonABCMeta, Initialized


class Capture(Enum):
    pipe = -1
    stdout = -2
    devnull = -3


class Completed(Initialized):
    """Contains the results of a command after being run."""
    def __init__(self, *, args: Sequence[str], returncode: int = 0,
                 stdout: str = None, stderr: str = None,
                 **super_kwargs) -> None:
        super().__init__(**super_kwargs)
        self.args = args
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr

    def check_returncode(self) -> None:
        if self.returncode:
            raise CommandError(self)


class CommandError(Exception):
    """Raised when a command returned an error code."""

    def __init__(self, completed: Completed) -> None:
        super().__init__('Command finished with error code {}'.format(
            completed.returncode))
        self.completed = completed


class Commander(metaclass=ABCMeta):
    """Abstract base class for objects that can run commands."""

    @abstractmethod
    def run_no_check(self, args: Sequence[str], **options) -> Completed:
        """Implement this method to run commands.

        Derived classes should implement this method to interpret
        the specified command according to their purpose. Client
        code interacting with a commander object should not invoke
        this method directly, however, but call :meth:`run` or
        :meth:`query` instead.
        """
        pass

    def run(self, *args, stdout: Any = None, stderr: Any = None,
            check: bool = False, **options) -> Completed:
        """Run a command and return its result.

        Note that the interface of this method intentionally mimics that
        of :meth:`subprocess.run`, except that the arguments are passed
        as a varargs parameter and that options may have different types.

        :param args: Command arguments. These will be converted to strings
            before being passed on, so for example integers are also fine.
        :param stdout: May either be a text output stream, ``None``, or
            one of the values ``Capture.pipe`` or ``Capture.devnull``.
        :param stderr: May either be a text output stream, ``None``, or
            a ``Capture`` value.
        :param check: If ``True``, the :meth:`Completed.check_returncode`
            method will be called on the return object, raising an
            exception in the case of a nonzero return code.
        :param options: Any keyword arguments to be passed on.
        :return: The result object from the executed command.
        """
        args = tuple(map(str, args))
        completed = self.run_no_check(args, stdout=stdout, stderr=stderr,
                                      **options)
        if check:
            completed.check_returncode()
        return completed

    def query(self, *args, **options) -> str:
        """Run a command and return text captured from stdout."""
        return self.run(*args, stdout=Capture.pipe, check=True,
                        **options).stdout


class Program(Commander, metaclass=ABCMeta):
    """Adapts the system interface of the running python script.

    Create a python program by deriving from this class and implementing
    the :meth:``Commander.run_no_check`` method. One thing you can do
    within this method is to call ``run`` or ``eval_sys`` on itself to
    restart the program with a different argument list.
    """

    def eval_sys(self, *extra_args) -> int:
        """Use the arguments passed to the running python script.

        :param extra_args: Further arguments to be added to the
            system arguments. To completely change the argument list,
            call the :meth:``Commander.run`` method instead.
        """
        args = list(sys.argv[1:])
        args += extra_args
        return self.run(*args).returncode

    def exec_sys(self) -> None:
        """Run the program and exit python after completion.

        Call this method in your main module to transfer execution
        of your python script to the `Program` object and pass the
        arguments to it that were passed to the script.
        """
        sys.exit(self.eval_sys())


class ModuleRunner(Commander, metaclass=SingletonABCMeta):
    """Adapts a python module to the `Commander` interface.

    The ``ModuleRunner()`` expression returns a `Commander` object
    whose :meth:`Commander.run` method expects the first argument
    to be a python module name. Invoking this method allows you to
    run any module as if it were the main module and capture its
    output and return value in the form of a `Completed` object.
    """

    def run_no_check(self, args: Sequence[str], stdout: Any = None,
                     stderr: Any = None, **options) -> Completed:
        """Runs a module as if it were the main module."""

        # Raise error if args is empty
        mod_name = args[0]

        # Raise error if capture
        for writer in stdout, stderr:
            if isinstance(writer, Capture):
                raise NotImplementedError('Capture not supported yet.')

        @contextmanager
        def replace_args():
            prev_args = sys.argv[1:]
            sys.argv[1:] = args[1:]
            yield
            sys.argv[1:] = prev_args

        with ExitStack() as stack:
            stack.enter_context(replace_args())
            if stdout is not None:
                stack.enter_context(redirect_stdout(stdout))
            if stderr is not None:
                stack.enter_context(redirect_stderr(stderr))
            try:
                run_module(mod_name, alter_sys=True)
            except SystemExit as err:
                code = err.code
            else:
                code = 0

        return Completed(args=args, returncode=code)
