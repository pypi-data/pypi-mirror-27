"""ABCs for the command line interface."""
from abc import abstractmethod, ABCMeta
from argparse import ArgumentParser
from io import StringIO
from pathlib import Path
from typing import Mapping, Any, Sequence, Iterable, Optional

from sav.bo import cmd
from sav.bo.apriori import check_unexpected_kwargs, Initialized, lazy_default
from sav.bo.cmd import Completed, Capture
from sav.bo.textio import StandardStreamsTuple
from sav.bo.terminals import (Terminal, RedirTerminal, SystemTerminal,
                              VerboseTerminal)


class Command(Initialized):
    """Base class for console command definitions."""

    def __init__(self, *, parser_options: Mapping[str, Any]=None,
                 **super_kwargs) -> None:
        super().__init__(**super_kwargs)
        self.parser_options: Mapping[str, Any] = lazy_default(parser_options,
                                                              dict)

    def config_parser(self, parser: ArgumentParser) -> None:
        """Configure the argument parser for this command.

        This implementation does nothing and acts both as
        the specification of the interface and as the root
        of any potential multiple inheritance diamond diagrams.
        All implementations of this method should invoke
        their super methods.
        """
        pass


class Performer(Command, metaclass=ABCMeta):
    """An object that can perform a command after it is parsed."""

    @abstractmethod
    def perform(self, parsed: Any, terminal: Terminal[Path]) -> Optional[int]:
        """Perform the command.

        :param terminal: The terminal to perform upon.
        :param parsed: The object returned by the parser.
        :return: Error code or None
        """
        return


class Program(Performer, cmd.Program, metaclass=ABCMeta):
    """Abstract base class for command-line programs."""

    def __init__(self, *, terminal: Terminal[Path]=None,
                 parser_options: Mapping[str, Any]=None,
                 **super_kwargs) -> None:
        super().__init__(parser_options=parser_options, **super_kwargs)
        self.terminal: Terminal[Path] = lazy_default(terminal, SystemTerminal)
        self.__parser: Optional[ArgumentParser] = None

    @property
    def parser(self) -> ArgumentParser:
        """Construct, configure, and cache the parser for reuse."""
        if self.__parser is None:
            p = ArgumentParser(**self.parser_options)
            self.config_parser(p)
            self.__parser = p
        return self.__parser

    def run_no_check(self, args: Sequence[str], stdout: Any = None,
                     stderr: Any = None, **unexpected_kwargs) -> Completed:
        """Implements :meth:`sav.bo.cmd.Commander.run_no_check`."""

        check_unexpected_kwargs(unexpected_kwargs)

        # Initialize local variables.
        params = stdout, stderr
        streams = [None, None]
        values = [None, None]
        redir_mode = (stdout is not None) or (stderr is not None)

        # Set up redirect mode
        # TODO: Use a context manager to handle shutdown with exceptions
        if redir_mode:
            for i, param in enumerate(params):
                streams[i] = StringIO() if param is Capture.pipe else param
            redir = StandardStreamsTuple(None, *streams)
            terminal = RedirTerminal(redir=redir,
                                     inner_term=self.terminal)
        else:
            terminal = self.terminal

        # Evaluate the command
        returncode = self.perform(self.parser.parse_args(args), terminal)
        if returncode is None:
            returncode = 0

        # Shut down redirect mode and collect values
        if redir_mode:
            for i, param in enumerate(params):
                if param is Capture.pipe:
                    values[i] = streams[i].getvalue()
                    streams[i].close()

        # Return result object
        return Completed(args=args, returncode=returncode,
                         stdout=values[0], stderr=values[1])


class Subcommand(Command):
    """A branch or leaf in the subcommand tree."""

    def __init__(self, *, name: str,
                 parser_options: Mapping[str, Any]=None,
                 **super_kwargs) -> None:
        super().__init__(parser_options=parser_options, **super_kwargs)
        self.name: str = name


class Supercommand(Command):
    """A collection of subcommands."""

    def __init__(self, *, subcommands: Iterable[Subcommand],
                 parser_options: Mapping[str, Any]=None,
                 **super_kwargs) -> None:
        super().__init__(parser_options=parser_options, **super_kwargs)
        self.subcommands = tuple(subcommands)

    def config_parser(self, parser: ArgumentParser) -> None:
        """Implements :meth:`Command.config_parser`."""
        super().config_parser(parser)
        subparsers = parser.add_subparsers()
        for subcommand in self.subcommands:
            subparser = subparsers.add_parser(subcommand.name,
                                              **subcommand.parser_options)
            subcommand.config_parser(subparser)


class Action(Subcommand, Performer, metaclass=ABCMeta):
    """A leaf in the subcommand tree."""

    def config_parser(self, parser: ArgumentParser) -> None:
        """Implements :meth:`Command.config_parser`.

        Subclasses should override this method to further
        configure their parsers. However, make sure they
        also invoke this implementation through a call to
        ``super()``.
        """
        super().config_parser(parser)
        parser.set_defaults(selected_action=self)


class Repertoire(Subcommand, Supercommand):
    """A branch of subcommands."""
    pass


class Agent(Program, Supercommand):
    """The root of a subcommand tree."""

    def perform(self, parsed: Any, terminal: Terminal[Path]):
        """Implements :meth:`Performer.perform`."""
        try:
            action = parsed.selected_action
        except AttributeError:
            terminal.print('No action selected.')
            return self.eval_sys('-h')
        else:
            return action.perform(parsed, terminal)


class VerboseCommand(Command):
    """Mixin class that adds verbosity handling to commands.

    You can mix this class with either :class:`sav.bo.cli.Program`
    to add the verbosity switch to a command line program or with
    :class:`sav.bo.cli.actions.Action` to add verbosity handling
    for a specific subcommand.
    """

    def config_parser(self, parser: ArgumentParser):
        """Implements :meth:`sav.bo.cli.Command.config_parser`."""
        super().config_parser(parser)
        parser.add_argument(
            "-v", "--verbosity",
            action="count", default=0,
            help="increase output verbosity")

    def perform(self, parsed: Any, terminal: Terminal[Path]):
        """Implements :meth:`sav.bo.cli.Performer.perform`."""
        vt = VerboseTerminal(verbosity=parsed.verbosity, inner_term=terminal)
        return self.perform_verbosity(parsed, vt)

    @abstractmethod
    def perform_verbosity(self, parsed: Any, terminal: Terminal[Path]):
        """Implement this method to construct your custom command.

        :param parsed: This will have a ``verbosity`` field.
        :param terminal: This will either be a
            :class:`sav.bo.terminals.verbosity.VerboseTerminal`
            or another terminal wrapped around it.
        """
        pass
