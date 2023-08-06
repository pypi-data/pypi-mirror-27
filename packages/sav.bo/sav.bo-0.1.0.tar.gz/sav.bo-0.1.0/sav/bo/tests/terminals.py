from collections import OrderedDict
from unittest import TestCase

from sav.bo.terminals import FifoTerminalBackend


def provide_input(file, text, end='\n'):
    offset = file.tell()
    print(text, file=file, end=end)
    file.seek(offset)


class TestFifoTerminalBackend(TestCase):

    def test_io(self):
        with FifoTerminalBackend() as backend:
            term = backend.terminal

            # Test print
            s = "Printing something."
            term.print(s)
            self.assertEqual(backend.out_reader.readline(), s + '\n')

            # Test input
            q, a = "Say something: ", 'something'
            print(a, file=backend.in_writer)
            x = term.input(q)
            self.assertEqual(x, a)
            self.assertEqual(backend.out_reader.readline(), q)

            # Test confirm
            print('bleep\ny', file=backend.in_writer)
            y = term.confirm("Did you say something?")
            self.assertIs(y, True)

            # Test choose
            print('7', file=backend.in_writer)
            alts = OrderedDict((('u', "Useful"), ('b', "Boring")))
            for i in range(10):
                alts[str(i)] = "Between(" + str(i) + ")"
            z = term.choose(
                'Was this test [u]seful, [b]oring, or '
                'somewhere in between [0-9]? ',
                alts)
            self.assertEqual(z, 'Between(7)')