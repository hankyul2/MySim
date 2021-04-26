import pytest

from MySim.src.cpu import CPU
from MySim.src.cse561sim import MySim


def test_construction():
    sim = MySim("./cse561sim 60 15 3 ../inputs/sample_input_gcc")
    cpu = CPU(60, 15, 3, sim.codes)
    assert 9 == len(cpu.registers)
    assert 0 == cpu.seq
    assert 0 == cpu.clock
    assert 0 == len(cpu.FE)


def test_run():
    sim = MySim("./cse561sim 60 15 3 ../inputs/sample_input_gcc")
    cpu = CPU(60, 15, 3, sim.codes)
    cpu.run()
    assert cpu.clock == 59
    assert cpu.seq == 100


def test_fetch():
    sim = MySim("./cse561sim 60 15 3 ../inputs/sample_input_gcc")
    cpu = CPU(60, 15, 3, sim.codes)
    assert True == cpu.fetch()
    assert 3 == len(cpu.DE)
    for seq, inst in enumerate(cpu.DE):
        assert 0 == inst.FE[0]
        assert 1 == inst.FE[1]
        assert 1 == inst.DE[0]
        assert seq == inst.seq_no


def test_decode():
    sim = MySim("./cse561sim 60 15 3 ../inputs/sample_input_gcc")
    cpu = CPU(60, 15, 3, sim.codes)
    assert True == cpu.fetch()
    assert True == cpu.decode()
    assert 0 == len(cpu.DE)
    assert 3 == len(cpu.RN)
    for inst in cpu.RN:
        assert 0 == inst.DE[1]
        assert 1 == inst.RN[0]


def test_rename():
    sim = MySim("./cse561sim 60 15 3 ../inputs/sample_input_gcc")
    cpu = CPU(60, 15, 3, sim.codes)
    assert True == cpu.fetch()
    assert True == cpu.decode()
    assert True == cpu.rename()
    assert 0 == len(cpu.DE)
    assert 0 == len(cpu.RN)
    assert 3 == len(cpu.DI)
    for inst in cpu.DI:
        assert inst.RN[1] == 0
        assert 1 == inst.DI[0]


def test_dispatch():
    sim = MySim("./cse561sim 60 15 3 ../inputs/sample_input_gcc")
    cpu = CPU(60, 15, 3, sim.codes)
    assert True == cpu.fetch()
    assert True == cpu.decode()
    assert True == cpu.rename()
    assert True == cpu.dispatch()
    assert 0 == len(cpu.DE)
    assert 0 == len(cpu.RN)
    assert 0 == len(cpu.DI)
    assert 3 == len(cpu.IQ)
    for inst in cpu.IQ:
        assert inst.DI[1] == 0
        assert inst.IS[0] == 1


def test_issue():
    sim = MySim("./cse561sim 60 15 3 ../inputs/sample_input_gcc")
    cpu = CPU(60, 15, 3, sim.codes)
    assert True == cpu.fetch()
    assert True == cpu.decode()
    assert True == cpu.rename()
    assert True == cpu.dispatch()
    assert True == cpu.issue()
    assert 0 == len(cpu.DE)
    assert 0 == len(cpu.RN)
    assert 0 == len(cpu.DI)
    assert 0 == len(cpu.IQ)
    assert 3 == len(cpu.RR)
    for inst in cpu.RR:
        assert inst.IS[1] == 0
        assert 1 == inst.RR[0]


def test_register_read():
    sim = MySim("./cse561sim 60 15 3 ../inputs/sample_input_gcc")
    cpu = CPU(60, 15, 3, sim.codes)
    assert True == cpu.fetch()
    assert True == cpu.decode()
    assert True == cpu.rename()
    assert True == cpu.dispatch()
    assert True == cpu.issue()
    assert True == cpu.register_read()
    assert 0 == len(cpu.DE)
    assert 0 == len(cpu.RN)
    assert 0 == len(cpu.DI)
    assert 0 == len(cpu.IQ)
    assert 0 == len(cpu.RR)
    assert 3 == len(cpu.EX)
    for inst in cpu.EX:
        assert inst.RR[1] == 0
        assert 1 == inst.EX[0]


@pytest.mark.skip(reason="This is not implemented yet")
def test_execute():
    sim = MySim("./cse561sim 60 15 3 ../inputs/sample_input_gcc")
    cpu = CPU(60, 15, 3, sim.codes)
    assert True == cpu.fetch()
    assert True == cpu.decode()
    assert True == cpu.rename()
    assert True == cpu.dispatch()
    assert True == cpu.issue()
    assert True == cpu.register_read()
    assert True == cpu.execute()
    assert 0 == len(cpu.DE)
    assert 0 == len(cpu.RN)
    assert 0 == len(cpu.DI)
    assert 0 == len(cpu.IQ)
    assert 0 == len(cpu.RR)
    assert 3 == len(cpu.WB)
    for inst in cpu.WB:
        assert -1 == inst.EX[1]
        assert 1 == inst.WB[0]


def test_advance_cycle():
    sim = MySim("./cse561sim 60 15 3 ../inputs/sample_input_gcc")
    cpu = CPU(60, 15, 3, sim.codes)
    for i in range(30):
        cpu.advance_cycle()
    assert 30 == cpu.clock
    assert True == cpu.advance_cycle()
