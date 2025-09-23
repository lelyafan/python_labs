op = []
alph = input().split()
if not alph:
    exit(ValueError)
for val in alph:
    if '.' in val:
        op.append(float(val))
    else:
        op.append(int(val))
print((min(op),max(op)))