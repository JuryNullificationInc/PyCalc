import pytest
from calc.lex import Lexer
from calc.objects import Process, SequentialRedex

l = Lexer()

program_1 = """z transits_over x.
  y receives_from x; x transits_over y; y receives_from x.
  v receives_from z; v transits_over v.
  v receives_from x; x transits_over x.
  """


class TestLex:

    def test_one(self):
        case1 = "x transits_over y."
        assert l.lex_expression(case1) == SequentialRedex(Process("x", "y", "TRANSMITTING"))

    def test_two(self):
        case1 = "x transits_over y"
        with pytest.raises(Exception):
            l.lex_expression(case1)

    def test_three(self):
        case1 = "x transits_over y; y receives_from y."
        assert l.lex_expression(case1) == SequentialRedex(Process("x", "y", "TRANSMITTING"), Process("y", "y", "LISTENING"))

    def test_lex_redexes(self):
        print(l.lex_redexes(program_1))

