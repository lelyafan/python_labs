def format_record(rec: tuple[str, str, float]) -> str:
    fio, gr, gpa = rec
    fio2 = ' '.join(fio.split()).split()
    fam = fio2[0]

    ini = []
    for i in range(1, len(fio2)):
        if i <= 2:
            ini.append(f'{fio2[i][0]}.')
    res = f'{fam} {' '.join(ini)}, гр. {gr}, GPA {gpa:.2f}'
    return res
t = ("Иванов Иван Иванович", "BIVT-25", 4.6)
print(format_record(t))