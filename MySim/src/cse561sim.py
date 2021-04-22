from MySim.src.cpu import CPU
from MySim.src.instruction import Instruction
from MySim.src.output_format import Output


class MySim:
    def __init__(self, command_line_string):
        self.argv = command_line_string
        self.ROB_SZ, self.IQ_SIZE, self.WIDTH = list(map(int, command_line_string.split(" ")[1:4]))
        self.input_path = command_line_string.split(" ")[4]
        self.read_trace()

    def read_trace(self):
        with open(self.input_path, 'rt') as f:
            trace = f.readlines()
            self.codes = [Instruction(inst) for inst in trace]

    def execute_program(self):
        cpu = CPU(self.codes)
        cpu.run()

        output = Output()
        for code in self.codes:
            output.insert_line(code)
        output.append_command(self.argv)
        output.append_simulation_result(30, 21)
        with open('../outputs/sample_output_gcc', 'wt') as f:
            f.writelines([out+"\n" for out in output.result])
        return len(output.result)


    



