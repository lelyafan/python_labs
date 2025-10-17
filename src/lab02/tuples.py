def format_record(rec: tuple[str, str, float]) -> str:
    try:
        fio, gr, gpa = rec
        fio2 = ' '.join(fio.split()).split()
        fam = fio2[0]

        if (fio not in rec) or (gr not in rec) or (gpa not in rec):
            return 'ValueError'

        ini = []
        for i in range(1, len(fio2)):
            if i <= 2:
                ini.append(f'{fio2[i][0]}.')
        res = f'{fam} {' '.join(ini)}, гр. {gr}, GPA {gpa:.2f}'
        return res
    except:
        return 'ValueError'
a = ("Иванов Иван Иванович", "BIVT-25", 4)
b = ("Петров Пётр", "IKBO-12", 5.0)
c = ("Петров Пётр Петрович", "IKBO-12", 5.0)
d = ("  сидорова  анна   сергеевна ", "ABB-01", 3.999)
f = ("СС", "", "")
print(format_record(a))
print(format_record(b))
print(format_record(c))
print(format_record(d))
print(format_record(f))
