#!/usr/bin/env python3

import sys

def ramp(routine, start_h, stop_h, start_T, stop_T, iterations):
    iterations = int(iterations)
    step_h = (stop_h - start_h) / iterations
    step_T = (stop_T - start_T) / iterations
    array = [[start_h + i * step_h, start_T + i * step_T] for i in range(iterations)]
    routine.extend(array)
    return array

field_rate = None
field_range = None
steps = None
iterations = None
mode = "loop"
start = None
stop = None

while sys.argv:
	if sys.argv[0] == "--rate":
		field_rate = float(sys.argv[1])
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--steps":
		steps = float(sys.argv[1])
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--start":
		start = float(sys.argv[1])
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--stop":
		stop = float(sys.argv[1])
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--iterations":
		iterations = int(sys.argv[1])
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--range":
		field_range = float(sys.argv[1])
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--mode":
		mode = sys.argv[1]
		sys.argv = sys.argv[1:]

	sys.argv = sys.argv[1:]

routine = []

if field_range != None:
	if field_rate != None:
		steps = int(field_range/field_rate)
		print(steps)
elif start != None and stop != None:
	if field_rate != None:
		steps = int(abs(stop-start)/field_rate)

if(mode == "loop"):
	if field_range == None or steps == None:
		print("Error: --range and --steps or --rate must be defined.")
		exit()
	else:
#		ramp(routine, 0, field_range, 6, 6, steps)
		print(steps)
		ramp(routine, field_range, -field_range, 6, 6, steps*2)
		ramp(routine, -field_range, field_range, 6, 6, steps*2)
		
if(mode == "half_loop"):
	if field_range == None or steps == None:
		print("Error: --range and --steps or --rate must be defined.")
		exit()
	else:
		ramp(routine, field_range, -field_range, 6, 6, steps)
		
if(mode == "range"):
	if start == None or stop == None:
		print("Error: --start, --stop and --steps or --rate must be defined.")
		exit()
	else:
		ramp(routine, start, stop, 6, 6, steps)
		
if(mode == "stepped_loop"):
	if field_range == None or steps == None or iterations == None:
		print("Error: --range, --iterations and --steps must be defined.")
		exit()
	else:
		for i in range(iterations):
			routine.append([field_range, 6])
		for field_entry in ramp([], field_range, -field_range, 6, 6, steps*2):
			for i in range(iterations):
				routine.append(field_entry)
		for field_entry in ramp([], -field_range, field_range, 6, 6, steps*2):
			for i in range(iterations):
				routine.append(field_entry)
		
if(mode == "const"):	
	if field_range == None or steps == None:
		print("Error: --range and --steps must be defined.")
		exit()
	else:
		ramp(routine, field_range, field_range, 6, 6, steps)

#Export
if field_range != None and field_rate != None:
	print(f"Writing field to field.dat. Rate: {round(field_rate,4)}, Range: {round(field_range,4)}")
else:
	print(f"Writing field to field.dat.")

with open("field.dat", "w") as f:
    f.write(f"{len(routine)} 2\n")
    for field, T in routine:
        f.write(f"{field} {T}\n")
