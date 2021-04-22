import pytest

from MySim.src.cse561sim import MySim


def test_construnction_parameter():
    sim = MySim("./cse561sim 60 15 3 ../inputs/sample_input_gcc")
    assert 60 == sim.ROB_SZ
    assert 15 == sim.IQ_SIZE
    assert 3 == sim.WIDTH

def test_read_trace():
    sim = MySim("./cse561sim 60 15 3 ../inputs/sample_input_gcc")
    assert 30 == len(sim.codes)

def test_execute_program_len():
    sim = MySim("./cse561sim 60 15 3 ../inputs/sample_input_gcc")
    assert 40 == sim.execute_program()

@pytest.mark.skip(reason="not implemented yet")
def test_execute_program_diff():
    sim = MySim("./cse561sim 60 15 3 ../inputs/sample_input_gcc")
    with open('../valid/sample_output_gcc', 'rt') as f:
        valid_output = f.readlines()

    with open('../outputs/sample_output_gcc', 'rt') as f:
        my_output = f.readlines()

    assert 40 == sim.execute_program()
    for out, val in zip(my_output, valid_output):
        assert out == val

