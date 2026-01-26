import sys

def ramp(start, stop, iterations):
    step = (stop - start) / iterations
    return [start + i * step for i in range(iterations)]

values = []

#Field routine
fieldRange = float(sys.argv[1])
rate = float(sys.argv[2]) #T/iteration

values.extend(ramp(0, fieldRange, int(fieldRange/rate)))
values.extend(ramp(fieldRange, -fieldRange, int(fieldRange*2/rate)))
values.extend(ramp(-fieldRange, fieldRange, int(fieldRange*2/rate)))

#values.extend(ramp(0, fieldRange, int(fieldRange/rate)))
#values.extend(ramp(fieldRange, -0.0, 1))
#values.extend(ramp(-0.0, -0.1, 10000))

#Export
with open("field.dat", "w") as f:
    f.write(f"{len(values)}\n")
    for v in values:
        f.write(f"{v}\n")
