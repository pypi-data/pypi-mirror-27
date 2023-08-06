import collections
from itertools import islice, cycle
from unittest import TestCase

from sav.bo.itertools import keymap, valmap, clustered, ClusterBufferError


class TestItertools(TestCase):

    def test_keymap(self):
        d = {1: 'Foo', 2: 'Bar'}
        # noinspection PyTypeChecker
        found = dict(keymap(str, d.items()))
        expected = {'1': 'Foo', '2': 'Bar'}
        self.assertEqual(expected, found)

    def test_valmap(self):
        d = {'Foo': 1, 'Bar': 2}
        # noinspection PyTypeChecker
        found = dict(valmap(str, d.items()))
        expected = {'Foo': '1', 'Bar': '2'}
        self.assertEqual(expected, found)

    def test_clustered(self):

        # sample clustering function
        def get_cat(val):
            if isinstance(val, int):
                if val:
                    return 'Positive' if val > 0 else 'Negative'
                return 'Zero'
            return 'Other'

        # First test: operate on lists
        sample = [1, 3, -1, 5, 0, -20, 0, 'Hello', 'Bye', -1]
        expected = [
            ('Positive', [1, 3, 5]),
            ('Negative', [-1, -20, -1]),
            ('Zero', [0, 0]),
            ('Other', ['Hello', 'Bye'])
        ]
        found = [(k, list(sub)) for k, sub in clustered(get_cat, sample)]
        self.assertEqual(expected, found)

        # Second test: operate on a fifo buffer
        sample_one, sample_two = sample[:5], sample[5:]

        # Create a fifo buffer with only half the input so far
        sample_fifo = collections.deque(sample_one)

        # Iterator which continues as values are appended
        def from_fifo():
            while sample_fifo:
                yield sample_fifo.popleft()

        # Get a clustered iterator for the buffer
        sample_iter = clustered(get_cat, from_fifo())

        # Get first two sub-iterators
        # This should consume the first three values, so two values
        # should remain in the fifo buffer at this point
        sub_iters = dict(islice(sample_iter, 2))
        self.assertEqual(len(sample_fifo), 2)

        # Get some values from first sub-iterator
        # To get the third positive value we need to consume one more
        # item from the fifo buffer, so one value should remain
        self.assertEqual(list(islice(sub_iters['Positive'], 3)), [1, 3, 5])
        self.assertEqual(len(sample_fifo), 1)

        # Add second half of the input
        sample_fifo += sample_two
        self.assertEqual(len(sample_fifo), 6)

        # Get some values from the second sub-iterator
        self.assertEqual(list(islice(sub_iters['Negative'], 2)), [-1, -20])
        self.assertEqual(len(sample_fifo), 4)

        # Get some values from the third sub-iterator
        k, sub = next(sample_iter)
        sub_iters[k] = sub
        self.assertEqual(list(islice(sub_iters['Zero'], 2)), [0, 0])
        self.assertEqual(len(sample_fifo), 3)

        # Consume remaining sub iterators
        # Of course, this should be only one
        # However, to determine that there is only one, all values should
        # now be read from the fifo buffer until it is empty
        for k, sub in sample_iter:
            sub_iters[k] = sub
        self.assertEqual(len(sub_iters), 4)
        self.assertEqual(len(sample_fifo), 0)

        # Check remaining values
        remaining = [
            ('Positive', []),
            ('Negative', [-1]),
            ('Zero', []),
            ('Other', ['Hello', 'Bye'])
        ]
        for k, sub in remaining:
            self.assertEqual(list(sub_iters[k]), sub)

        # Third test: operate on infinite iterator
        sample_iter = clustered(get_cat, cycle(sample), buffer_max=100)
        sub_iters = {}
        with self.assertRaises(ClusterBufferError):
            for k, sub in sample_iter:
                sub_iters[k] = sub

        # These iterators exist but are no longer valid
        self.assertEqual(len(sub_iters), 4)
