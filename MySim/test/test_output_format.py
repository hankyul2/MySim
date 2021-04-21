from MySim.src.output_format import Output


def test_construction():
    assert Output()


def test_make_line():
    output = Output()
    output.insert_line(0, [29, 14], -1, [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1]])
    assert "0 fu{0} src{29,14} dst{-1} FE{0,1} DE{1,1} RN{2,1} DI{3,1} IS{4,1} RR{5,1} EX{6,1} WB{7,1} CM{8,1}" \
           == output.result[0]


def test_append_command():
    output = Output()
    output.append_command("./cse561sim 60 15 3 traces/sample_input_gcc")
    assert 6 == len(output.result)


def test_append_simulation_result():
    output = Output()
    output.append_simulation_result(30, 21)
    assert 4 == len(output.result)
    assert "# Instructions Per Cycle    = 1.43" == output.result[3]
