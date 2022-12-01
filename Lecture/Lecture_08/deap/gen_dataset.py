import random
import csv
import pathlib

NBR_ITEMS = 20

filepath = pathlib.Path(__file__).parent / "dataset.csv"

data = []

for i in range(NBR_ITEMS):
    data.append((random.randint(1, 10), random.uniform(0, 100)))

with open(filepath, 'w', newline='') as fo:
    csvwriter = csv.writer(fo)
    csvwriter.writerows(data)

with open(filepath, 'r') as fo:
    csv_reader = csv.reader(fo)
    for row in csv_reader:
        print(row[0])
