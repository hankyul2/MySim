class CPU:
    def __init__(self, codes):
        self.codes = codes
        self.seq = 0
        self.clock = 0
        self.registers = [[] for i in range(9)]

    def run(self):
        pass

    @property
    def FE(self):
        return self.registers[0]

    @property
    def DE(self):
        return self.registers[1]

    @property
    def RN(self):
        return self.registers[2]

    @property
    def DI(self):
        return self.registers[3]

    @property
    def IS(self):
        return self.registers[4]

    @property
    def RR(self):
        return self.registers[5]

    @property
    def EX(self):
        return self.registers[6]

    @property
    def WB(self):
        return self.registers[7]

    @property
    def CM(self):
        return self.registers[8]
