import os
import csv
import sys


iter = sys.argv[1]

thread_counts = [1,2,4,8]

rows = []

print("iter :" + iter)

for i in thread_counts:
    for j in iter:
        os.system("./sequential_test.out 1 100000 1000 .99 .005 .005 > output.txt")

        with open("test.txt", "r") as f:
            outputs = f.read().splitlines()
            count = outputs[1].split(":")[1].strip()
            time = outputs[2].split(":")[1].strip()
            rows.append([count, time])
            

print(rows)