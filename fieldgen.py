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

while sys.argv:
	if sys.argv[0] == "--rate":
		field_rate = float(sys.argv[1])
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--range":
		field_range = float(sys.argv[1])
		sys.argv = sys.argv[1:]

	sys.argv = sys.argv[1:]

routine = []

if field_range != None and field_rate != None:
	steps = int(field_range/field_rate)

#Loop
ramp(routine, field_range, field_range, 6, 6, steps)
ramp(routine, field_range, -field_range, 6, 6, steps*2)
ramp(routine, -field_range, field_range, 6, 6, steps*2)

##Positive
#ramp(routine, 0, 6, 25, 6, 480)
#ramp(routine, 6, 2, 6, 6, 200)

#ramp(routine, 2, 2, 6, 6, 200)

#ramp(routine, 2, -2, 6, 6, 400)
#ramp(routine, -2, 2, 6, 6, 400)

##Negative
#ramp(routine, -6, -6, 25, 6, 200)
#ramp(routine, -6, -2, 6, 6, 200)

#ramp(routine, -2, -2, 6, 6, 200)

#ramp(routine, -2, 2, 6, 6, 400)
#ramp(routine, 2, -2, 6, 6, 400)

#values.extend(ramp(fieldRange, fieldRange, int(fieldRange/rate)))
#values.extend(ramp(fieldRange, -fieldRange, int(fieldRange*2/rate)))
#values.extend(ramp(-fieldRange, fieldRange, int(fieldRange*2/rate)))

#values.extend(ramp(0, fieldRange, int(fieldRange/rate)))
#values.extend(ramp(fieldRange, -0.0, 1))
#values.extend(ramp(-0.0, 0.0, 1000))

#Export
print(f"Writing field to field.dat. Rate: {round(field_rate,4)}, Range: {round(field_range,4)}")
with open("field.dat", "w") as f:
    f.write(f"{len(routine)} 2\n")
    for field, T in routine:
        f.write(f"{field} {T}\n")
