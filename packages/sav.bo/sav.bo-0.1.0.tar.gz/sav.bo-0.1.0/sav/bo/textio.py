import sys
from abc import ABCMeta, abstractmethod
from collections import Sequence
from io import TextIOBase, StringIO, SEEK_END
from typing import Any, List, MutableSequence, Optional

from sav.bo.apriori import Initialized, lazy_default, SingletonABCMeta


class Writable(TextIOBase, metaclass=ABCMeta):
    """ABC for writable text streams."""

    @abstractmethod
    def writetext(self, s: str) -> None:
        """Implement this method to create a writable text stream."""
        pass

    def write(self, s: str) -> int:
        """Implementation of :meth:`io.TextIOBase.write`.

        :return: The length of ``s``.

            The specification of :meth:`io.TextIOBase.write` requires
            that we return the number of characters written, in order
            to preserve consistency with :meth:`io.RawIOBase.write`
            and :meth:`io.BufferedIOBase.write`, which both return
            the number of bytes written.

            Note, however, that this return value is only really
            meaningful in the case of :meth:`io.RawIOBase.write`.
            When a raw stream is opened in non-blocking mode, an
            implementation of this method is supposed to return
            the number of bytes actually written when it failed
            to write all the bytes that were passed to it.

            By contrast, when buffered binary and text streams need
            to flush their buffers in non-blocking mode, any failure
            to write all characters without blocking is supposed to
            raise a :exc:`BlockingIOError` and store the number of
            characters actually written in the
            :attr:`BlockingIOError.characters_written` attribute.
            Hence, whenever an implementation of
            :meth:`io.BufferedIOBase.write` or
            :meth:`io.TextIOBase.write` does return without raising
            an error, its return value must by definition always
            equal the number of bytes or characters that were passed
            to it.

            Since the caller already knows this number before calling
            our method, this return value seems to be useful only
            in dynamic or generic contexts where the caller might be
            writing to both raw and buffered streams without
            distinction. Although such use cases seem rare, we shall
            conform to the interface by returning the length of the
            argument, while delegating the actual writing to the
            abstract :meth:`writetext` method, which specifies no
            return value.

        """
        self.writetext(s)
        return len(s)

    def writable(self) -> bool:
        return True


class Appender(Writable):
    """Append written text to a sequence.

    This adapts the sequence interface to the writable interface.

    ..  attribute:: data

        Sequence that written text is appended to.

    """
    def __init__(self, data: MutableSequence[str] = None,
                 **super_kwargs) -> None:
        super().__init__(**super_kwargs)
        self.data = lazy_default(data, list)

    def writetext(self, s: str) -> None:
        self.data.append(s)


class OuterStream(Initialized, TextIOBase):
    """Base class for wrappers around text streams.

    Note that this is different from :class:`io.TextIOWrapper`, which
    is a text wrapper around a binary stream.

    ..  attribute:: inner_stream

        The inner text stream object. We use duck typing because which
        methods this object needs to provide depends on the situation.

    ..  attribute:: close_inner

        Whether to close the inner stream when the outer stream is
        closed. False by default.

    """

    def __init__(self, inner_stream: Any, **super_kwargs) -> None:
        super().__init__(**super_kwargs)
        self.inner_stream = inner_stream
        self.close_inner: bool = False

    def close(self) -> None:
        super().close()
        if self.close_inner:
            self.inner_stream.close()


class OuterWritable(OuterStream, Writable):
    """Base class for writable wrappers around text streams.

    ..  attribute:: direct_writelines

        If this is `True`, then our :meth:`writelines` method will
        directly write to the inner stream. Otherwise it will
        delegate to the :meth:`writetext` method of the outer stream.

        Note that if your derived outer stream class overrides
        the :meth:`writetext` method, then a value of `True` would
        cause :meth:`writelines` to bypass the functionality of your
        modified :meth:`writetext` method. Therefore, the default value
        of this field is `False`.

        Classes which allow the outer :meth:`writetext` method to call
        the outer :meth:`writelines` method should typically set this
        field to `True` in order to prevent infinite loops.

    """

    def __init__(self, inner_stream: Any, **super_kwargs) -> None:
        super().__init__(inner_stream=inner_stream, **super_kwargs)
        self.direct_writelines: bool = False

    def writetext(self, s: str) -> None:
        self.inner_stream.write(s)

    def writelines(self, lines: List[str]) -> None:
        if self.direct_writelines:
            try:
                self.inner_stream.writelines(lines)
            except AttributeError:
                for line in lines:
                    self.inner_stream.write(line)
        else:
            super().writelines(lines)


class LineWriter(OuterWritable):
    """Line-buffered text writer.

    Text written to this stream is split into lines and written
    to the inner stream`s ``writelines`` method (if available) or
    written to its ``write`` method one line at a time. If the last
    character written to this stream before it is closed was not a
    line ending, then all remaining characters are passed on to the
    inner stream`s ``write`` method.
    """

    def __init__(self, inner_stream: Any, **super_kwargs) -> None:
        super().__init__(inner_stream=inner_stream, **super_kwargs)
        self.direct_writelines = True
        self.__line_buffer: Optional[StringIO] = None

    def writetext(self, s: str) -> None:
        """Split text into different lines before writing them.

        :param s: The text to be split into lines. Characters beyond
            the last newline character will be buffered. The buffer
            is either combined with characters before the next newline
            in subsequent strings passed to this method, or written
            to the inner stream when this stream is closed.
        """

        # Return directly if there is nothing to be written.
        if not s:
            return

        # This will return at least one line of text.
        lines = s.splitlines(keepends=True)

        # Invoke the splitlines method again, without keepends this
        # time, upon the last line in the list, to strip any
        # newline characters at the end of it if there were any.
        # This trick ensures consistency with whatever list of
        # newline characters the splitlines method might employ.
        stripped_last_line = lines[-1].splitlines()[0]

        # If the stripped line equals the unstripped line, then our
        # last line did not end with a newline character.
        has_residue = (stripped_last_line == lines[-1])

        # Remove the residue from the lines to be written.
        if has_residue:
            lines.pop()

        # Write all lines that have newline characters.
        if lines:
            self.writelines(lines)

        # Write the residue to the buffer
        if has_residue:
            if self.__line_buffer is None:
                self.__line_buffer = StringIO()
            self.__line_buffer.write(stripped_last_line)

    def writelines(self, lines: List[str]) -> None:
        """Write lines to the inner stream.

        :param lines: A list of strings. Each string must end with a
            line ending and contain no other line endings. This also
            means none of the strings can be empty. The list may be
            empty however. If both this list and the current line
            buffer are non-empty, a copy of the list will be made
            and the contents of the line buffer will be prepended
            to the first line.
        """
        if not lines:
            return
        lb = self.__line_buffer
        if lb is not None:
            lines = lines[:]
            lb.write(lines[0])
            lines[0] = lb.getvalue()
            lb.close()
            self.__line_buffer = None
        super().writelines(lines)

    def close(self):
        """Flush line buffer and close the stream."""
        lb = self.__line_buffer
        if lb is not None:
            self.inner_stream.write(lb.getvalue())
            lb.close()
        super().close()


class Fifo(OuterWritable):
    """Text stream wrapper implementing a FIFO buffer.

    Writes to an inner stream without advancing its position,
    allowing the text to be read back from the inner stream.

    ..  attribute:: inner_stream

        The inner stream, inherited from :class:`OuterStream`,
        should be readable and writable, and will by
        default be a :class:`io.StringIO` buffer.


    ..  attribute:: close_inner

        Inherited from :class:`OuterStream`, but `True` by default
        instead of `False`. Thus, if no inner stream is passed to
        our constructor and a new string buffer is opened when
        our stream is opened, then that buffer will also be closed
        when our stream is closed. In most cases this is desirable,
        since a FIFO buffer is meant to be read from while it is
        still open for writing on the other end.

    """

    def __init__(self, inner_stream: Any = None, **super_kwargs) -> None:
        super().__init__(inner_stream=lazy_default(inner_stream, StringIO),
                         **super_kwargs)
        self.close_inner = True

    def writetext(self, s: str) -> None:
        """Write to the end of the inner stream."""

        inner = self.inner_stream
        offset = inner.tell()     # Save current position
        inner.seek(0, SEEK_END)   # Move to end of stream
        inner.write(s)            # Write text at the end
        inner.seek(offset)        # Move back to saved position


class StandardStreams(Sequence):

    def __len__(self) -> int:
        return 3

    @property
    def stdin(self) -> Any:
        return self[0]

    @property
    def stdout(self) -> Any:
        return self[1]

    @property
    def stderr(self) -> Any:
        return self[2]


class StandardStreamsTuple(tuple, StandardStreams):

    def __new__(cls, stdin: Any = None, stdout: Any = None,
                stderr: Any = None):
        return tuple.__new__(cls, (stdin, stdout, stderr))


class RedirStreams(Initialized, StandardStreams):

    def __init__(self, *, redir: StandardStreams,
                 default: StandardStreams, **super_kwargs) -> None:
        super().__init__(**super_kwargs)
        self.redir = redir
        self.default = default

    def __getitem__(self, item: int) -> Any:
        return lazy_default(self.redir[item], lambda: self.default[item])


class SystemStreams(StandardStreams, metaclass=SingletonABCMeta):

    def __getitem__(self, item: int) -> Any:
        return getattr(sys, ('stdin', 'stdout', 'stderr')[item])