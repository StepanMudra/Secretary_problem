import Structure
import os
import time
import csv

tic = time.perf_counter()
elements_for_permutations = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
max_test_set_length = len(elements_for_permutations)
max_number_of_valuating = max_test_set_length
def fill_structures():
    s = []
    for test_set in range(1, max_test_set_length):
        for valuating in range(1, test_set + 1):
            s.append(Structure.Structure(test_set, valuating))
    return s
structures = fill_structures()
path = "Results/"
for s in structures:
    for file in os.listdir(path):
        with open(path+file, 'r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                if str(s.test_set) == line[0] and str(s.evaluation_value) == line[1]:
                    for i in range(14):
                        s.values[i] += int(line[(i+2)])
def results(structures):
    for sez in structures:
        with open('Summarized_results.csv', 'a', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([sez.test_set, sez.evaluation_value] + sez.values)
results(structures)