import sys
sys.path.insert(0, ".")
from MySim.src.cse561sim import MySim

sim = MySim(" ".join(sys.argv))
sim.execute_program(debug=True)
