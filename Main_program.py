import itertools
import csv
import Structure
import multiprocessing
import math

elements_for_permutations = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
max_test_set_length = len(elements_for_permutations)
max_number_of_valuating = max_test_set_length
def fill_structures():
    s = []
    for test_set in range(1, max_test_set_length):
        for valuating in range(1, test_set + 1):
            s.append(Structure.Structure(test_set, valuating))
    return s
def calculations(size, remaining, i, elements_for_permutations):
    index_start = i * size
    if remaining > 0:
        index = index_start + size + remaining
    else:
        index = index_start + size
    permutations = itertools.islice(itertools.permutations(elements_for_permutations, len(elements_for_permutations)), index_start, index)
    structures = fill_structures()  # Each process has its own copy
    for permutation in permutations:
        for u in range(len(structures)):
            k = 0
            testing_pool = sorted(permutation[:structures[u].test_set])
            value = testing_pool[structures[u].evaluation_value - 1]
            for element in permutation[structures[u].test_set:]:
                index = structures[u].elements.index(element)
                if element > value:
                    structures[u].values[index] += 1
                    break
                elif k == len(elements_for_permutations) - 1:
                    structures[u].values[index] += 1
                k += 1
    # Send local structures to file
    results(structures, i)
def results(structures, i):
    for structure in structures:
        with open('Results/results' + str(i) + '.csv', 'a', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([structure.test_set, structure.evaluation_value] + structure.values)
if __name__ == '__main__':
    num_processes = 48
    permutations_count = math.factorial(len(elements_for_permutations))
    chunk_size = permutations_count // num_processes
    remaining = permutations_count - (chunk_size * num_processes)

    # Start the processes
    processes = []
    for i in range(num_processes):
        if i == num_processes - 1:
            p = multiprocessing.Process(target=calculations, args=(chunk_size, remaining, i, elements_for_permutations))
        else:
            p = multiprocessing.Process(target=calculations, args=(chunk_size, 0, i, elements_for_permutations))
        processes.append(p)
        p.start()