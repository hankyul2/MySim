from MySim.src.instruction import Instruction
from MySim.src.output_format import Output


def test_construction():
    assert Output()


def test_make_line():
    inst = Instruction("2b6420 0 -1 29 14")
    output = Output()
    output.insert_line(inst)
    assert "0 fu{0} src{29,14} dst{-1} FE{0,0} DE{0,0} RN{0,0} DI{0,0} IS{0,0} RR{0,0} EX{0,0} WB{0,0} CM{0,0}" \
           == output.result[0]


def test_append_command():
    output = Output()
    output.append_command("./cse561sim 60 15 3 ../inputs/sample_input_gcc")
    assert 6 == len(output.result)


def test_append_simulation_result():
    output = Output()
    output.append_simulation_result(30, 21)
    assert 4 == len(output.result)
    assert "# Instructions Per Cycle    = 1.43" == output.result[3]
