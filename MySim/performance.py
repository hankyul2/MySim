import sys
import matplotlib.pyplot as plt
import pandas as pd
sys.path.insert(0, ".")
from MySim.src.cse561sim import MySim

test_range = list(range(1, 10))
rob_list = []
iq_list = []
width_list = []
ip_list = []

for ROB in test_range:
    for IQ in test_range:
        for WIDTH in test_range:
            print(ROB, IQ, WIDTH)
            sim = MySim("MySim/main.py {} {} {} inputs/val_trace_gcc1".format(ROB, IQ, WIDTH))
            _, IPC = sim.execute_program()
            rob_list.append(ROB)
            iq_list.append(IQ)
            width_list.append(WIDTH)
            ip_list.append(IPC)

df = pd.DataFrame({"ROB":rob_list, "IQ":iq_list, "WIDTH":width_list, "IPC":ip_list})
df.to_csv("search_1")