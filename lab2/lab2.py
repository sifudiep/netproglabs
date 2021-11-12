lines = ""
with open('score2.txt') as txtFile:
    lines = txtFile.readlines()

persons = {}

for line in lines:
    lineData = line.split(" ")
    personName = lineData[2] + " " + lineData[3]
    if personName in persons:
        persons[personName] += int(lineData[4])
    else:
        persons[personName] = int(lineData[4])

winnerName = ""
highestScore = 0

for person in persons:
    if (persons[person] > highestScore): 
        highestScore = persons[person]
        winnerName = person

print(f"The winner is : {winnerName} with a score of : {highestScore}")