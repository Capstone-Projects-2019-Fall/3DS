import re

output = open("output.txt", "w")
for line in open ('pos.txt', 'r').readlines():
    string=line.replace(".0", "")
    print(string)
    output.write(string)
output.close()
