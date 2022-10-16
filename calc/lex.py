from . import objects

Process = objects.Process
SeqRedex = objects.SequentialRedex
ParallelRedex = objects.ParallelRedex
Terminal = objects.TerminalProcess()


class Lexer:

    keywords = ["transits_over", "fresh", "receives_from"]

    def __init__(self):
        pass

    def lex_redexes(self, text_in):
        batch = text_in.strip().split("\n")
        batch = [self.lex_expression(x) for x in batch]
        result = ParallelRedex()
        [result.compose(x) for x in batch]
        return result


    def lex_expression(self, text_in):

        result = SeqRedex()

        if '.' not in text_in:
            raise Exception("Expressions must be terminated with .")
        else:
            text_in = text_in.strip('.')

        batch = text_in.split(";")
        for chunk in batch:
            chunk = chunk.strip().split(" ")

            if len(chunk) != 3:
                raise Exception("Expression must be of form %VAR %OP %VAR")

            match chunk:
                case [symbol, "transits_over", channel]:
                    p = Process(symbol, channel, "TRANSMITTING")
                    p.transmit(symbol, channel)
                    result.append(p)
                case [symbol, "receives_from", channel]:
                    p = Process(symbol, channel, "LISTENING")
                    p.receive(symbol, channel)
                    result.append(p)

        result.append(Terminal)
        return result



