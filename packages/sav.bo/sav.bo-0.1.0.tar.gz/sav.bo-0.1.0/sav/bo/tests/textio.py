from unittest import TestCase

from sav.bo.textio import Fifo, Appender, LineWriter


class TestText(TestCase):

    def test_line_writer(self):
        listw = Appender()
        expected, found = [], listw.data
        with LineWriter(inner_stream=listw) as writer:

            # Input without newline characters
            writer.write('Fi')
            writer.write('rst li')

            # Empty input
            writer.write('')

            # Newline character in the middle
            writer.write('ne.\nSec')
            expected.append('First line.\n')
            self.assertEqual(expected, found)

            # Newline character at the end
            writer.write('ond line.\n')
            expected.append('Second line.\n')
            self.assertEqual(expected, found)

            # Multiple newline characters
            writer.write('Third line.\nFourth line.\nFifth line.')
            expected.append('Third line.\n')
            expected.append('Fourth line.\n')
            self.assertEqual(expected, found)

            # Only a newline character
            writer.write('\n')
            expected.append('Fifth line.\n')
            self.assertEqual(expected, found)

            # Close without newline character at the end
            writer.write('Sixth line.')

        expected.append('Sixth line.')
        self.assertEqual(expected, found)

        with LineWriter(inner_stream=listw) as writer:

            # Close with newline character at the end
            writer.write('Seventh line.\n')

        expected.append('Seventh line.\n')
        self.assertEqual(expected, found)

    def test_fifo(self):
        with Fifo() as writer:
            reader = writer.inner_stream
            print('Yo', file=writer)
            self.assertEqual(reader.readline(), 'Yo\n')
            print('Second line.', file=writer)
            self.assertEqual(reader.readline(), 'Second line.\n')
