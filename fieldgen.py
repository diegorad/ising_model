def ramp(start, stop, iterations):
    step = (stop - start) / iterations
    return [start + i * step for i in range(iterations)]

values = []

#Field routine
values.extend(ramp(0, 6, 200))
values.extend(ramp(6, -6, 400))
values.extend(ramp(-6, 6, 400))

#Export
with open("field.dat", "w") as f:
    f.write(f"{len(values)}\n")
    for v in values:
        f.write(f"{v}\n")
