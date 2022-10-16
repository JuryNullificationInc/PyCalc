import random


class Process:
    def __repr__(self):
        return f"<{self.symbol} {self.status} {self.channel}>"

    def __str__(self):
        return f"<{self.symbol} {self.status} {self.channel}>"

    def __eq__(self, other):
        return (self.symbol, self.channel, self.status) == (
            other.symbol,
            other.channel,
            other.status,
        )

    def __init__(self, symbol, channel, status):
        self.symbol = symbol
        self.channel = channel
        self.status = status

    def transmit(self, symbol, channel):
        self.status = "TRANSMITTING"
        self.symbol = symbol
        self.channel = channel

    def receive(self, symbol, channel):
        self.status = "LISTENING"
        self.symbol = symbol
        self.channel = channel


class TerminalProcess(Process):
    def __repr__(self):
        return "□"

    def __str__(self):
        return "□"

    def __init__(self):
        self.symbol = 0
        self.channel = 0
        self.status = 0


class SequentialRedex:
    def __repr__(self):
        return f"||{self.processes.__repr__()}||"

    def __eq__(self, other):
        if type(other) != SequentialRedex:
            return False

        if len(self) == len(other):
            return all([self[x] == other[x] for x in range(len(self))])

    def __len__(self):
        return len(self.processes)

    def __getitem__(self, item):
        return self.processes[item]

    def __init__(self, *processes):
        self.terminated = False
        self.processes = list(processes)

    def append(self, *process):
        self.processes.append(process)

    def head(self):
        head = self.processes.pop(0)
        setattr(head, "body", self)
        return head

    def is_terminated(self):
        if self.processes == [TerminalProcess()]:
            self.terminated = True
            return True


class ParallelRedex:
    def __repr__(self):
        return f"?{self.redexes.__repr__()}?"

    def __len__(self):
        return len(self.redexes)

    def __eq__(self, other):
        if type(other) != ParallelRedex:
            return False

        truthy = []
        if len(self) == len(other):
            for redex in self.redexes:
                if redex in other.redexes:
                    truthy.append(
                        True
                    )  # needs to be fixed later, this will fail on some edge cases

        return all(truthy)

    def __getitem__(self, item):
        return self.redexes[item]

    def __init__(self, *redexes):
        self.redexes = list(redexes)

    def compose(self, redex):
        if type(redex) != ParallelRedex and type(redex) != SequentialRedex:
            raise Exception(
                "Parallel Redexes can only be composed with Parallel and Sequential Redexes"
            )

        self.redexes.append(redex)

    def execute_once(self):
        heads = []
        for redex in self.redexes:
            if not redex.is_terminated():
                heads.append(redex.head())

        channel_equivalence_cells = {}
        for head in heads:
            if head.channel not in channel_equivalence_cells:
                channel_equivalence_cells[head.channel] = {
                    "TRANSMITTING": [],
                    "LISTENING": [],
                }

            match head.status:
                case "TRANSMITTING":
                    channel_equivalence_cells[head.channel]["TRANSMITTING"] += [
                        head.symbol
                    ]
                case "LISTENING":
                    channel_equivalence_cells[head.channel]["LISTENING"] += [head.body]

        for channel in channel_equivalence_cells:
            transmitted_values = channel_equivalence_cells[channel]["TRANSMITTING"]
            listening_agents = channel_equivalence_cells[channel]["LISTENING"]
            for agent in listening_agents:
                if not transmitted_values:
                    pass
                else:
                    agent[0].symbol = random.choice(transmitted_values)

        return str(channel_equivalence_cells)

    def all_are_terminated(self):
        return all([x.is_terminated() for x in self.redexes])

    def execute(self):
        stacktrace = []
        i = 0
        while not self.all_are_terminated():
            step = self.execute_once()
            print(i, step)
            stacktrace.append(step)
            i += 1
        return stacktrace
