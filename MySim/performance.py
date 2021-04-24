import sys
import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, ".")
from MySim.src.cse561sim import MySim

base_range = list(range(1, 20))
power_range = [pow(2, i) for i in range(10)]
rob_list = []
iq_list = []
width_list = []
ip_list = []

for ROB in power_range:
    for IQ in power_range:
        for WIDTH in base_range:
            sim = MySim("MySim/main.py {} {} {} inputs/val_trace_gcc1".format(ROB, IQ, WIDTH))
            _, IPC = sim.execute_program()
            print("MySim/main.py {} {} {} inputs/val_trace_gcc1 : {}".format(ROB, IQ, WIDTH, IPC))
            rob_list.append(ROB)
            iq_list.append(IQ)
            width_list.append(WIDTH)
            ip_list.append(IPC)

df = pd.DataFrame({"ROB": rob_list, "IQ": iq_list, "WIDTH": width_list, "IPC": ip_list})
df.to_csv("search_1")
