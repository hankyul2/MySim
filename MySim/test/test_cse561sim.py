from MySim.src.cse561sim import MySim


def test_construnction_parameter():
    sim = MySim(10, 10, 5)
    assert 10 == sim.ROB_SZ
    assert 10 == sim.IQ_SIZE
    assert 5 == sim.WIDTH

def test_read_trace():
    sim = MySim(10, 10, 5)
    sim.read_trace('../inputs/sample_input_gcc')
    assert 30 == len(sim.codes)

def test_execute_program():
    sim = MySim(10, 10, 5)
    sim.read_trace('../inputs/sample_input_gcc')
    assert 40 == sim.execute_program("./cse561sim 60 15 3 traces/sample_input_gcc")
