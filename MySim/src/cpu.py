from collections import deque
from typing import List, Deque

from MySim.src.instruction import Instruction

ARCH_REGISTER_NUM = 67
PHYS_REGISTER_NUM = ARCH_REGISTER_NUM * 2
# READY Constant
YES = 1
NO = 0
FREE = -1
# IQ Constant
NOT_READY = 0
READY = 1
# ROB Constant
NOT_YET = 0
DONE = 1


class CPU:
    def __init__(self, ROB, IQ, WIDTH, codes: List[Instruction]):
        self.RMT = [reg_no for reg_no in range(ARCH_REGISTER_NUM)]
        self.READY = [YES for _ in range(ARCH_REGISTER_NUM)] + [FREE for _ in range(ARCH_REGISTER_NUM)]
        self.ROB: Deque[Instruction] = deque(maxlen=ROB)
        self.IQ: Deque[Instruction] = deque(maxlen=IQ)
        self.WIDTH = WIDTH
        self.codes = codes
        self.seq = 0
        self.clock = 0
        self.registers = [[] for i in range(9)]
        self.latency = [0, 1, 4]
        self.output = list()
        self.trace_len = len(codes)

    @property
    def FE(self) -> List[Instruction]:
        return self.registers[0]

    @property
    def DE(self) -> List[Instruction]:
        return self.registers[1]

    @property
    def RN(self) -> List[Instruction]:
        return self.registers[2]

    @property
    def DI(self) -> List[Instruction]:
        return self.registers[3]

    @property
    def IS(self) -> List[Instruction]:
        return self.registers[4]

    @property
    def RR(self) -> List[Instruction]:
        return self.registers[5]

    @property
    def EX(self) -> List[Instruction]:
        return self.registers[6]

    @property
    def WB(self) -> List[Instruction]:
        return self.registers[7]

    @WB.setter
    def WB(self, value):
        self.registers[7] = value

    @property
    def CM(self) -> List[Instruction]:
        return self.registers[8]

    def run(self):
        while True:
            self.commit()
            self.write_back()
            self.execute()
            self.register_read()
            self.issue()
            self.dispatch()
            self.rename()
            self.decode()
            self.fetch()
            if not self.advance_cycle():
                break
        self.clock -= 1

    def check_code_len(self):
        if len(self.codes) + len(self.ROB) + len(self.DE) + len(self.RN) + len(self.output) != self.trace_len:
            raise Exception("Code misses", self.clock, len(self.codes), len(self.ROB), len(self.output), self.trace_len)

    def advance_cycle(self):
        self.check_code_len()
        self.clock += 1
        return bool(self.codes) or any([bool(pipe) for pipe in self.registers]) or len(self.ROB)

    def fetch(self):
        if not self.codes or self.DE:
            return False
        fe_len = self.WIDTH if len(self.codes) >= self.WIDTH else len(self.codes)
        for i in range(fe_len):
            self.codes[0].FE[0] = self.clock
            self.codes[0].FE[1] = 1
            self.codes[0].DE[0] = self.clock + 1
            self.codes[0].seq_no = self.seq
            self.seq += 1
            self.DE.append(self.codes.pop(0))
        return True

    def decode(self):
        if self.RN:
            return False
        while self.DE:
            self.DE[0].DE[1] = self.clock - self.DE[0].DE[0] + 1
            self.DE[0].RN[0] = self.clock + 1
            self.RN.append(self.DE.pop(0))
        return True

    def rename(self):
        if self.DI:
            return False
        while self.register_available():
            inst = self.RN[0]
            inst.phys_src1 = self.RMT[inst.arch_src1] if inst.arch_src1 != -1 else -1
            inst.phys_src2 = self.RMT[inst.arch_src2] if inst.arch_src2 != -1 else -1
            if inst.arch_dest != -1:
                inst.old_phys_dest = self.RMT[inst.arch_dest]
                new_phys_dest = self.get_new_register()
                if False == new_phys_dest:
                    return False
                self.RMT[inst.arch_dest] = new_phys_dest
                inst.phys_dest = new_phys_dest
            else:
                inst.old_phys_dest = -1
                inst.phys_dest = -1
            self.RN.pop(0)
            self.ROB.append(inst)
            inst.RN[1] = self.clock - inst.RN[0] + 1
            inst.DI[0] = self.clock + 1
            self.DI.append(inst)
        return True

    def get_new_register(self):
        i = 0
        for i, status in enumerate(self.READY):
            if status == FREE:
                self.READY[i] = YES
                return i
        return False

    def dispatch(self):
        # Todo: It can dispatch instruction to IQ until Instruction Queue is not fully occupied
        while self.DI and len(self.IQ) < self.IQ.maxlen:
            self.DI[0].DI[1] = self.clock - self.DI[0].DI[0] + 1
            self.DI[0].IS[0] = self.clock + 1
            if self.DI[0].phys_dest != -1:
                self.READY[self.DI[0].phys_dest] = NO
            self.IQ.append(self.DI.pop(0))
        return True

    def issue(self):
        if self.RR:
            return False

        ready_pair = list()

        for i, inst in enumerate(self.IQ):
            if (inst.phys_src1 == -1 or self.READY[inst.phys_src1]) and (
                    inst.phys_src2 == -1 or self.READY[inst.phys_src2]):
                inst.ready = READY
                ready_pair.append(inst)

        ready_pair.sort(key=lambda x: x.seq_no, reverse=False)
        ready_len = self.WIDTH if len(ready_pair) >= self.WIDTH else len(ready_pair)

        for i in range(ready_len):
            inst = ready_pair[i]
            if inst.phys_dest != -1:
                self.READY[inst.phys_dest] = YES
            inst.IS[1] = self.clock - inst.IS[0] + 1
            inst.RR[0] = self.clock + 1
            self.IQ.remove(inst)
            self.RR.append(inst)

        return True

    def register_read(self):
        while self.RR:
            self.RR[0].RR[1] = self.clock - self.RR[0].RR[0] + 1
            self.RR[0].EX[0] = self.clock + 1
            self.EX.append(self.RR.pop(0))
        return True

    def execute(self):
        self.WB = list(filter(lambda x: self.clock - x.EX[0] == self.latency[x.op_type], self.EX))
        for x in self.WB:
            x.EX[1] = self.clock - x.EX[0] + 1
            x.WB[0] = self.clock + 1
            self.EX.remove(x)
        return True

    def write_back(self):
        while self.WB:
            self.WB[0].Done = DONE
            self.WB[0].WB[1] = self.clock - self.WB[0].WB[0] + 1
            self.WB[0].CM[0] = self.clock + 1
            self.CM.append(self.WB.pop(0))
        return True

    def commit(self):
        commit_len = self.WIDTH if len(self.ROB) > self.WIDTH else len(self.ROB)
        for i in range(commit_len):
            if self.ROB[0].Done == DONE:
                self.ROB[0].CM[1] = self.clock - self.ROB[0].CM[0] + 1
                if self.ROB[0].old_phys_dest != -1:
                    self.READY[self.ROB[0].old_phys_dest] = FREE
                self.CM.remove(self.ROB[0])
                self.output.append(self.ROB.popleft())
            else:
                break
        return True

    def register_available(self):
        # Todo: Precalculate how many registers are available -> it only make complicate structure
        # Todo: if it push instruction to ROB in rename stage, it should check ROB size in rename stage. -> Good!
        if bool(self.RN) and len(self.ROB) < self.ROB.maxlen:
            return True
        else:
            return False
