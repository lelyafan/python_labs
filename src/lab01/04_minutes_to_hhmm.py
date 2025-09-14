m = int(input())
print(f'Минуты: {m:02d}')
hours = m // 60
minutes = m % 60
print(f'{hours}:{minutes}')