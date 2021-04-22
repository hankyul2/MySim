from dataclasses import dataclass, field


@dataclass
class Instruction:
    str_inst: str

    phys_dest: int = field(default=0)
    phys_src1: int = field(default=0)
    phys_src2: int = field(default=0)

    old_phys_dest: int = field(default=0)

    seq_no: int = field(default=0)

    registers: int = field(default_factory=lambda: [[0, 0] for reg in range(9)])

    @property
    def pc(self):
        return hex(self.str_inst.split(" ")[0])

    @property
    def op_type(self):
        return int(self.str_inst.split(" ")[1])

    @property
    def arch_dest(self):
        return int(self.str_inst.split(" ")[2])

    @property
    def arch_src1(self):
        return int(self.str_inst.split(" ")[3])

    @property
    def arch_src2(self):
        return int(self.str_inst.split(" ")[4])

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





