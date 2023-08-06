import os
import shutil
import stat
from abc import abstractmethod
from collections import OrderedDict
from io import StringIO
from pathlib import Path
from subprocess import PIPE, STDOUT, DEVNULL, run
from typing import TypeVar, Any, Iterable, Mapping, Generic, Sequence

from sav.bo.apriori import Initialized, lazy_default, SingletonGenericMeta
from sav.bo.cmd import Commander, Completed, Capture
from sav.bo.names import enum_names
from sav.bo.textio import (Fifo, StandardStreams, StandardStreamsTuple,
                           RedirStreams, SystemStreams)

PathT = TypeVar('PathT')


class Terminal(Commander, Generic[PathT]):
    """Terminal interface.

    This abstract base class defines methods for text-based input,
    output, and subprocesses.
    """

    @property
    @abstractmethod
    def streams(self) -> StandardStreams:
        pass

    @property
    @abstractmethod
    def cwd(self) -> PathT:
        """A path object to the terminal's current working directory."""
        pass

    @cwd.setter
    @abstractmethod
    def cwd(self, value: PathT) -> None:
        pass

    @abstractmethod
    def get_path(self, *pathsegments) -> PathT:
        pass

    @abstractmethod
    def walk(self, root: PathT) -> Iterable[PathT]:
        pass

    @abstractmethod
    def rmtree(self, path: PathT, **options) -> None:
        pass

    @abstractmethod
    def print(self, *objects, file: Any = None, **options) -> None:
        pass

    @abstractmethod
    def input(self, prompt: Any = None, stdin: Any = None,
              stdout: Any = None) -> str:
        pass

    def choose(self, prompt: Any, alternatives: Mapping[str, Any],
               caseless: bool = True) -> Any:
        """Ask the user to choose from alternatives.

        The alternatives argument should be a mapping from
        accepted possible input strings to possible return values.
        """
        adjusted = (
            OrderedDict(
                ((k.casefold(), v) for k, v in alternatives.items()))
            if caseless else alternatives)
        altlist = None
        while True:
            inputstr = self.input(prompt)
            key = inputstr.casefold() if caseless else inputstr
            try:
                return adjusted[key]
            except KeyError:
                self.print('Choice not recognized:', repr(inputstr))
                if not altlist:
                    altlist = list(alternatives.keys())
                    prompt = "Please enter '{}' or '{}': ".format(
                        "', '".join(altlist[:-1]), altlist[-1])

    def confirm(self, prompt: str, infix: str = ' (y/n) ',
                caseless: bool = True) -> bool:
        return self.choose(
            prompt + infix, OrderedDict([('y', True), ('n', False)]),
            caseless)


def remove_readonly(func, path, _):
    """Clear the readonly bit and reattempt the removal"""
    os.chmod(path, stat.S_IWRITE)
    func(path)


class _OutputHandler:
    """Helper class that handles an output or error stream.

    ..  attribute:: passed

        The value that was passed to the ``stdout`` or ``stderr``
        parameter of :meth:`SystemTerminal.run`.

    ..  attribute:: hasfileno

        Whether the output stream has a file desriptor.

    """

    def __init__(self, passed: Any) -> None:
        self.passed = passed
        try:
            passed.fileno()
        except (OSError, AttributeError):
            self.hasfileno = False
        else:
            self.hasfileno = True

    @property
    def arg(self) -> Any:
        """The argument to be passed to the subprocess library.

        Returns the value that should be passed to the ``stdout``
        or ``stderr`` parameter of :func:`subprocess.run`.
        """

        conversion = {Capture.pipe: PIPE,
                      Capture.stdout: STDOUT,
                      Capture.devnull: DEVNULL}

        if self.passed is None:
            # No stream redirection
            return None
        elif isinstance(self.passed, Capture):
            # Convert special value
            return conversion[self.passed]
        elif self.hasfileno:
            # Filedescriptor stream
            # We pass this on and let the OS handle it
            return self.passed
        else:
            # Non-filedescriptor stream
            # We will capture this and redirect manually
            return PIPE

    def convert_result(self, result: Any) -> Any:
        if (result is not None) and (self.passed is not Capture.pipe):
            self.passed.write(result)
            return None
        else:
            return result


class SystemTerminal(Terminal[Path], metaclass=SingletonGenericMeta):
    """System terminal interface.

    Stateless singleton object which provides the standard
    interface by wrapping around the print and subprocess
    library functions.
    """

    @property
    def streams(self) -> SystemStreams:
        return SystemStreams()

    @property
    def cwd(self) -> Path:
        return Path.cwd()

    @cwd.setter
    def cwd(self, value) -> None:
        os.chdir(str(value))

    def get_path(self, *pathsegments) -> Path:
        return Path(*pathsegments)

    def walk(self, root):
        for path_str, dirnames, filenames in os.walk(str(root)):
            yield self.get_path(path_str), dirnames, filenames

    def rmtree(self, path, onerror=remove_readonly, **options):
        shutil.rmtree(str(path), onerror=onerror, **options)

    def print(self, *objects, file=None, **options):
        if file is not None:
            options['file'] = file
        print(*objects, **options)

    def input(self, prompt=None, stdin=None, stdout=None):
        if prompt is not None:
            if (stdin is None) and (stdout is None):
                return input(prompt)
            else:
                stdout.write(prompt)
        if stdin is None:
            return input()
        line = stdin.readline()
        if line == '':
            raise EOFError()
        return line.rstrip('\r\n')

    # noinspection PyMethodMayBeStatic
    def run_no_check(self, args: Sequence[str], stdout: Any = None,
                     stderr: Any = None, cwd: Any = None,
                     **options) -> Completed:
        oh, eh = _OutputHandler(stdout), _OutputHandler(stderr)
        if cwd is not None:
            options['cwd'] = str(cwd)
        completed = run(args, stdout=oh.arg, stderr=eh.arg,
                        universal_newlines=True, **options)
        return Completed(args=args, returncode=completed.returncode,
                         stdout=oh.convert_result(completed.stdout),
                         stderr=eh.convert_result(completed.stderr))


class OuterTerminal(Initialized, Terminal[PathT]):
    def __init__(self, *, inner_term: Terminal = None, **super_kwargs) -> None:
        super().__init__(**super_kwargs)
        self.inner_term = lazy_default(inner_term, SystemTerminal)

    def run_no_check(self, args: Sequence[str], **options) -> Completed:
        return self.inner_term.run_no_check(args, **options)

    @property
    def streams(self) -> StandardStreams:
        return self.inner_term.streams

    def print(self, *objects, **options) -> None:
        self.inner_term.print(*objects, **options)

    def input(self, prompt: Any = None, stdin: Any = None,
              stdout: Any = None) -> str:
        return self.inner_term.input(prompt, stdin, stdout)

    @property
    def cwd(self) -> Any:
        return self.inner_term.cwd

    @cwd.setter
    def cwd(self, value: Any) -> None:
        self.inner_term.cwd = value

    def get_path(self, *pathsegments) -> Any:
        return self.inner_term.get_path(*pathsegments)

    def walk(self, root: Any) -> Iterable:
        return self.inner_term.walk(root)

    def rmtree(self, path: Any, **options) -> None:
        self.inner_term.rmtree(path, **options)


class RedirTerminal(OuterTerminal):

    def __init__(self, *, redir: StandardStreams, **super_kwargs) -> None:
        super().__init__(**super_kwargs)
        self._streams = RedirStreams(redir=redir, default=super().streams)

    @property
    def streams(self) -> StandardStreams:
        return self._streams

    def print(self, *objects, file: Any = None, **options) -> None:
        super().print(
            *objects,
            file=lazy_default(file, lambda: self._streams.redir.stdout),
            **options
        )

    def input(self, prompt: Any = None, stdin: Any = None,
              stdout: Any = None) -> str:
        return super().input(
            prompt,
            lazy_default(stdin, lambda: self._streams.redir.stdin),
            lazy_default(stdout, lambda: self._streams.redir.stdout)
        )

    def run_no_check(self, args: Sequence[str], stdout: Any = None,
                     stderr: Any = None, **options) -> Completed:
        return super().run_no_check(
            args,
            stdout=lazy_default(stdout, lambda: self._streams.redir.stdout),
            stderr=lazy_default(stderr, lambda: self._streams.redir.stderr),
            **options
        )


class FifoTerminalBackend(Initialized):

    def __init__(self, *, inner_term: Terminal = None,
                 **super_kwargs) -> None:
        super().__init__(**super_kwargs)
        self.in_writer = Fifo()
        redir = StandardStreamsTuple(self.in_writer.inner_stream,
                                     Fifo(), Fifo())
        self.terminal = RedirTerminal(inner_term=inner_term, redir=redir)

    @property
    def out_reader(self) -> StringIO:
        return self.terminal.streams.stdout.inner_stream

    @property
    def err_reader(self) -> StringIO:
        return self.terminal.streams.stderr.inner_stream

    def __enter__(self) -> 'FifoTerminalBackend':
        return self

    # noinspection PyUnusedLocal
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def close(self) -> None:
        self.in_writer.close()
        self.terminal.streams.stdout.close()
        self.terminal.streams.stderr.close()

    def to_inner(self) -> None:
        self.terminal.inner_term.streams.stdout.write(self.out_reader.read())
        self.terminal.inner_term.streams.stderr.write(self.err_reader.read())


class WorkDirTerminal(OuterTerminal):
    """A terminal that maintains its own working directory."""

    def __init__(self, *, work_dir: Any = None, **super_kwargs) -> None:
        super().__init__(**super_kwargs)
        self.work_dir = lazy_default(work_dir, lambda: self.inner_term.cwd)

    def run_no_check(self, args: Sequence[str], cwd: Any = None,
                     **options) -> Completed:
        return super().run_no_check(
            args,
            cwd=lazy_default(cwd, lambda: self.work_dir),
            **options
        )

    @property
    def cwd(self) -> Any:
        return self.work_dir

    @cwd.setter
    def cwd(self, value) -> None:
        self.work_dir = value


Verbosity = enum_names('normal, verbose, logging, debug')


class VerboseTerminal(OuterTerminal):
    def __init__(self, *, verbosity: int = Verbosity.normal,
                 **super_kwargs) -> None:
        super().__init__(**super_kwargs)
        self.verbosity = verbosity

    def print(self, *objects, verbosity: int = Verbosity.normal,
              **options) -> None:
        if self.verbosity >= verbosity:
            super().print(*objects, **options)

    def run_no_check(self, args: Sequence[str], **options) -> Completed:
        self.print("Calling subprocess:", args, verbosity=Verbosity.logging)
        return super().run_no_check(args, **options)
