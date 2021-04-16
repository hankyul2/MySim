from dataclasses import dataclass


@dataclass
class Instruction:
    str_inst: str

    phys_dest: int
    phys_src1: int
    phys_src2: int

    old_phys_dest: int

    @property
    def pc(self):
        return hex(self.str_inst.split(" ")[0])

    @property
    def op_type(self):
        return hex(self.str_inst.split(" ")[1])

    @property
    def arch_dest(self):
        return hex(self.str_inst.split(" ")[2])

    @property
    def arch_src1(self):
        return hex(self.str_inst.split(" ")[3])

    @property
    def arch_src2(self):
        return hex(self.str_inst.split(" ")[4])




