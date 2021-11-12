lines = ""
with open('diary.txt') as f:
    lines = f.readlines()

for line in lines:
    print(line)