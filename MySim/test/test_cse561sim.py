import pytest

from MySim.src.cse561sim import MySim


def test_construnction_parameter():
    sim = MySim("./cse561sim 60 15 3 ../inputs/sample_input_gcc")
    assert "../inputs/sample_input_gcc" == sim.input_path
    assert 60 == sim.ROB_SZ
    assert 15 == sim.IQ_SIZE
    assert 3 == sim.WIDTH


def test_read_trace():
    sim = MySim("./cse561sim 60 15 3 ../inputs/sample_input_gcc")
    assert 30 == len(sim.codes)


def test_execute_program_len():
    sim = MySim("./cse561sim 60 15 3 ../inputs/sample_input_gcc")
    assert 40 == sim.execute_program('../outputs/sample_output_gcc')

def test_execute_program_len2():
    sim = MySim("./cse561sim 256 64 40 ../inputs/val_trace_gcc1")
    assert 10010 == sim.execute_program('../outputs/val_output_gcc1')

def test_execute_program_len3():
    sim = MySim("./cse561sim 256 64 40 ../inputs/val_trace_perl1")
    assert 10010 == sim.execute_program('../outputs/val_output_perl1')


@pytest.mark.skip(reason="There is bugs in sample output files")
def test_execute_program_diff():
    sim = MySim("./cse561sim 60 15 3 ../inputs/sample_input_gcc")
    assert 40 == sim.execute_program('../outputs/sample_output_gcc')
    with open('../valid/sample_output_gcc', 'rt') as f:
        valid_output = f.readlines()

    with open('../outputs/sample_output_gcc', 'rt') as f:
        my_output = f.readlines()

    for out, val in zip(my_output, valid_output):
        assert out == val


@pytest.mark.skip(reason="There is bugs in sample output files")
def test_execute_program_diff2():
    sim = MySim("./cse561sim 128 16 5 ../inputs/sample_input_perl")
    assert 40 == sim.execute_program('../outputs/sample_output_perl')
    with open('../valid/sample_output_perl', 'rt') as f:
        valid_output = f.readlines()

    with open('../outputs/sample_output_perl', 'rt') as f:
        my_output = f.readlines()

    for out, val in zip(my_output, valid_output):
        assert out == val
