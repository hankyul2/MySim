from MySim.src.cpu import CPU
from MySim.src.cse561sim import MySim


def test_construction():
    sim = MySim("./cse561sim 60 15 3 ../inputs/sample_input_gcc")
    cpu = CPU(sim.codes)
    assert 9 == len(cpu.registers)
    assert 0 == cpu.seq
    assert 0 == cpu.clock
    assert 0 == len(cpu.FE)


def test_run():
    sim = MySim("./cse561sim 60 15 3 ../inputs/sample_input_gcc")
    cpu = CPU(sim.codes)
    cpu.run()
