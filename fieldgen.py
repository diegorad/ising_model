import sys

def ramp(routine, start_h, stop_h, start_T, stop_T, iterations):
    iterations = int(iterations)
    step_h = (stop_h - start_h) / iterations
    step_T = (stop_T - start_T) / iterations
    routine.extend(
    	[[start_h + i * step_h, start_T + i * step_T] for i in range(iterations)]
    )
    return

routine = []

#Field routine
fieldRange = float(sys.argv[1])
rate = float(sys.argv[2]) #T/iteration
steps = int(fieldRange/rate)

ramp(routine, -6, -6, 25, 6, 200)
ramp(routine, -6, -2.5, 6, 6, 200)
ramp(routine, -2.5, -2.5, 6, 6, 200)
#ramp(routine, 0, 2.5, 6, 6, 200)
ramp(routine, -2.5, 2.5, 6, 6, 400)
ramp(routine, 2.5, -2.5, 6, 6, 400)

ramp(routine, -2.5, 2.5, 6, 6, 400)
ramp(routine, 2.5, -2.5, 6, 6, 400)

ramp(routine, -2.5, 2.5, 6, 6, 400)
ramp(routine, 2.5, -2.5, 6, 6, 400)


#values.extend(ramp(fieldRange, fieldRange, int(fieldRange/rate)))
#values.extend(ramp(fieldRange, -fieldRange, int(fieldRange*2/rate)))
#values.extend(ramp(-fieldRange, fieldRange, int(fieldRange*2/rate)))

#values.extend(ramp(0, fieldRange, int(fieldRange/rate)))
#values.extend(ramp(fieldRange, -0.0, 1))
#values.extend(ramp(-0.0, 0.0, 1000))

#Export
with open("field.dat", "w") as f:
    f.write(f"{len(routine)} 2\n")
    for field, T in routine:
        f.write(f"{field} {T}\n")
