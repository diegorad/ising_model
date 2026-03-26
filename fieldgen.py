#!/usr/bin/env python3

import sys

def ramp(routine, start_h, stop_h, start_T, stop_T, iterations):
    iterations = int(iterations)
    step_h = (stop_h - start_h) / iterations
    step_T = (stop_T - start_T) / iterations
    routine.extend(
    	[[start_h + i * step_h, start_T + i * step_T] for i in range(iterations)]
    )
    return

field_rate = None
field_range = None
steps = None

while sys.argv:
	if sys.argv[0] == "--rate":
		field_rate = float(sys.argv[1])
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--steps":
		steps = float(sys.argv[1])
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--range":
		field_range = float(sys.argv[1])
		sys.argv = sys.argv[1:]

	sys.argv = sys.argv[1:]

routine = []

if field_range != None and field_rate != None:
	steps = int(field_range/field_rate)

##Loop
ramp(routine, field_range, field_range, 6, 6, steps)
ramp(routine, field_range, -field_range, 6, 6, steps*2)
ramp(routine, -field_range, field_range, 6, 6, steps*2)

#Constant
#ramp(routine, field_range, field_range, 6, 6, steps)

#Custom

#Export
if field_range != None and field_rate != None:
	print(f"Writing field to field.dat. Rate: {round(field_rate,4)}, Range: {round(field_range,4)}")
else:
	print(f"Writing field to field.dat.")

with open("field.dat", "w") as f:
    f.write(f"{len(routine)} 2\n")
    for field, T in routine:
        f.write(f"{field} {T}\n")
