from MySim.src.instruction import Instruction


def test_construction():
    assert Instruction("2b6420 0 -1 29 14")

def test_register_file():
    inst = Instruction("2b6420 0 -1 29 14")
    assert 9 == len(inst.registers)
    assert 2 == len(inst.FE)
    assert 0 == inst.FE[0]
    inst.FE[0] = 3
    assert 3 == inst.FE[0]


