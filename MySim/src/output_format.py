class Output:
    def __init__(self):
        self.attr_list = ["FE", "DE", "RN", "DI", "IS", "RR", "EX", "WB", "CM"]
        self.result = []

    def insert_line(self, op_type, src, dest, pipe_lines):
        line_num = len(self.result)
        op_line = "{} fu{{{}}} src{{{}}} dst{{{}}}".format(line_num, op_type, ",".join(map(str, src)), dest)
        stage_line = [stage + "{{{}}}".format(",".join(map(str, value))) for stage, value in
                      zip(self.attr_list, pipe_lines)]
        self.result.append(op_line + " " + " ".join(stage_line))

    def append_command(self, cmd_arg):
        self.result.append("# === Simulator Command =========")
        self.result.append("# " + cmd_arg)
        self.result.append("# === Processor Configuration ===")
        self.result.append("# ROB_SIZE = {}".format(cmd_arg.split()[1]))
        self.result.append("# IQ_SIZE  = {}".format(cmd_arg.split()[2]))
        self.result.append("# WIDTH    = {}".format(cmd_arg.split()[3]))

    def append_simulation_result(self, inst_cnt, cycle):
        self.result.append("# === Simulation Results ========")
        self.result.append("# Dynamic Instruction Count = {}".format(inst_cnt))
        self.result.append("# Cycles                    = {}".format(cycle))
        self.result.append("# Instructions Per Cycle    = {:.3}".format(inst_cnt/cycle))