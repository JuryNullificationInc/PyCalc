import pytest
from calc.lex import Lexer
from calc.objects import Process, TerminalProcess, SequentialRedex, ParallelRedex

Terminal = TerminalProcess()

p1 = Process("x", "y", "TRANSMITTING")
p2 = Process("y", "y", "LISTENING")
p3 = Process("z", "y", "LISTENING")

ex1 = Process("z", "x", "TRANSMITTING")
ex2 = Process("y", "x", "LISTENING")
ex3 = Process("x", "y", "TRANSMITTING")
ex4 = Process("y", "x", "LISTENING")
ex5 = Process("v", "z", "LISTENING")
ex6 = Process("v", "v", "TRANSMITTING")
ex7 = Process("v", "x", "LISTENING")
ex8 = Process("x", "x", "TRANSMITTING")

sr1 = SequentialRedex(Terminal)
sr2 = SequentialRedex(p1, p2, Terminal)
sr3 = SequentialRedex(p3, Terminal)

sr_ex1 = SequentialRedex(ex1, Terminal)
sr_ex2 = SequentialRedex(ex2, ex3, ex4, Terminal)
sr_ex3 = SequentialRedex(ex5, ex6, Terminal)
sr_ex4 = SequentialRedex(ex7, ex8, Terminal)

pr1 = ParallelRedex()
pr2 = ParallelRedex(sr2, sr3)

ex_pr1 = ParallelRedex(sr_ex1, sr_ex2, sr_ex3, sr_ex4)


class TestProcess:

    def test_process_equality(self):
        assert p3 == Process("y", "y", "TRANSMITTING")


class TestSequentialRedex:

    def test_array_equality(self):
        x = sr1
        x.append(p1)
        x.append(p2)
        y = sr2
        assert x == y

    def test_subitem_equality(self):
        assert sr2[1] == p2
        assert sr2.head() == p1

    def test_three(self):
        assert sr2.head() == p1


class TestParallelRedex:

    def test_array_equality(self):
        x = pr1
        x.compose(sr1)
        x.compose(sr2)
        assert x == pr2

    def test_parallel_repr(self):
        print(ex_pr1)

    def test_execute_once(self):
        print(ex_pr1.execute_once())

    def test_execute(self):
        print(ex_pr1.execute())
