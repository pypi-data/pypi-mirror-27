from unittest import TestCase

from sav.bo.cli import Action, Repertoire, Agent


class Bar(Action):

    def __init__(self):
        super().__init__(name='bar')

    latest_x = None

    def config_parser(self, parser):
        super().config_parser(parser)
        parser.add_argument("x")

    def perform(self, parsed, terminal):
        super().perform(parsed, terminal)
        Bar.latest_x = parsed.x


class Baz(Action):

    def __init__(self):
        super().__init__(name='baz')

    def config_parser(self, parser):
        super().config_parser(parser)
        parser.add_argument("y")

    def perform(self, parsed, terminal):
        return super().perform(parsed, terminal)


def create_foo_repertoire():
    return Repertoire(
        name='foo', subcommands=(Bar(), Baz()),
        parser_options=dict(help='This is the foo help intro text')
    )


def create_agent():
    return Agent(
        subcommands=(
            create_foo_repertoire(),
        ),
        parser_options=dict(
            prog='fancy',
            description='Fancy program'
        )
    )


class TestAgent(TestCase):

    def test_repertoire(self):
        create_agent().run('foo', 'bar', 'pete', check=True)
        self.assertEqual(Bar.latest_x, 'pete')
