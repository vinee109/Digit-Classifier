import numpy, scipy
import sys
import csv
import struct

DIGIT_WIDTH = 28
DIGIT_HEIGHT = 28

def get_input_data(data_source):
    """
    Gets the data from a given csv file and converts each line into a list of numbers
    """
    def convert_to_int(lst):
        new = []
        for i in lst:
            if float(i) > 0:
                new.append(1)
            else:
                new.append(0)
        return new

    data = []
    with open(data_source, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            vec = numpy.array(convert_to_int(row))
            # adding extra feature: number of contiguous white regions
            vec = numpy.append(vec, [num_white_regions(vec)])
            data.append(vec)
    return data

def get_input_labels(data_source):
    """
    Gets the labels from a given csv file and converts each line into a list of numbers
    """
    data = []
    with open(data_source, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            data.append(int(row[0]))
    return data 

def print_digit(row):
    """
    Prints a digit based on the values for each pixel, given in its features. Used mainly
    for debugging purposes
    """
    string = ''
    for j in range(DIGIT_HEIGHT):
        for i in range(DIGIT_WIDTH):
            if row[j + DIGIT_WIDTH*i] > 0:
                string += '1'
            else:
                string += '0'
        string += '\n'
    print string

def euclidean_distance(vec1, vec2):
    """
    Calculates the euclidean_distance between two vectors
    >>> vec1 = numpy.array([0, 0, 0, 0])
    >>> vec2 = numpy.array([1, 1, 1, 1])
    >>> euclidean_distance(vec1, vec2)
    2.0
    """
    return numpy.linalg.norm(vec1 - vec2)

def classify(vector, trainingDataLabels, k):
    # values = []
    heap = struct.BinaryHeap(k, lambda x: x[1])
    for key in trainingDataLabels:
        key_vec = numpy.array(list(key))
        dist = euclidean_distance(vector, key_vec)
        # values.append(dist)
        heap.insert((key, dist))
    lowest_items = heap.get_items()
    
    counts = [ 0 for i in range(0, 10)]
    for item in lowest_items:
        vec = item[0]
        counts[trainingDataLabels[vec]] += 1
    return determine_max(vector, counts)
    # print sorted(values)[:k]

def determine_max(vector, counts):
    max_count = max(counts)
    indices = [i for i in range(len(counts)) if counts[i] == max_count]
    return indices[0]

# attempt at implementing some extra features
def num_white_regions(vector):
    """
    Runs depth-first search to calculate the number of white regions in a particular vector
    """
    def dfs(start, visited, allPixels):
        if start in visited or start not in allPixels:
            return
        x, y = start
        visited.add(start)
        # go in all directions
        dfs((x+1, y), visited, allPixels)
        dfs((x-1, y), visited, allPixels)
        dfs((x, y-1), visited, allPixels)
        dfs((x, y+1), visited, allPixels)
        dfs((x+1, y+1), visited, allPixels)
        dfs((x-1, y+1), visited, allPixels)
        dfs((x+1, y-1), visited, allPixels)
        dfs((x-1, y-1), visited, allPixels)

    # count number of black regions
    allPixels = set([(x, y) for y in range(DIGIT_HEIGHT) for x in range(DIGIT_WIDTH) if vector[y + DIGIT_WIDTH*x] == 0])
    visited = set()
    num_regions = 0
    for p in list(allPixels):
        if p not in visited:
            num_regions += 1
            dfs(p, visited, allPixels)
    return num_regions

def train(data_source, label_source):
    print 'Training........'
    data = get_input_data(data_source)
    labels = get_input_labels(label_source)
    train_label_map = { tuple(data[i]) : labels[i] for i in range(len(data))}
    return train_label_map

def validate(train_data_source, train_label_source, val_data_source, val_label_source, k, output=False):
    training_labels = train(train_data_source, train_label_source)
    print 'Importing Validation Data........'
    val_data = get_input_data(val_data_source)
    val_labels = get_input_labels(val_label_source)
    print 'Validating..........'
    guesses = []
    count = 1
    for vec in val_data:
        if count % 20 == 0:
            print 'Completed', count
        guesses.append(classify(vec, training_labels, k))
        count += 1
    print 'Verifying...........'
    num_correct, total = check_error(val_data, guesses, val_labels)
    print 'Number correct ' + str(num_correct) + ' out of ' + str(total) 
    print 'Percentage: ' + str(float(num_correct)/float(total) * 100) + '%'
    print 'Error Rate: ' + str((float(total) - float(num_correct))/float(total) * 100) + '%'
    if output:
        output_file(guesses, k)

def check_error(vector_data, guesses, correctLabels):
    num_correct = 0
    for i in range(len(guesses)):
        if guesses[i] == correctLabels[i]:
            num_correct += 1
        # uncomment if you want to see which ones are incorrect
        else:
            print_digit(vector_data[i])
            print 'Iteration', i
            print 'Guess', guesses[i]
            print 'Correct', correctLabels[i]
    return num_correct, len(guesses)

def test(train_data_source, train_label_source, test_data_source, k):
    print 'Testing.........'
    training_labels = train(train_data_source, train_label_source)
    data = get_input_data(test_data_source)
    guesses = [classify(vec, training_labels, k) for vec in data]
    output_file(guesses, None)

def output_file(data, k):
    """
    Output the guesses for data with the value k
    """
    if k:
        filename = 'digitsOutput' + str(k) + '.csv'
    else:
        filename = 'digitsOutput.csv'
    f = open(filename, 'w')
    for line in data:
        f.write(str(line) + '\n')
    f.close()

def parseCommand(args):
    from optparse import OptionParser
    parser = OptionParser('')
    parser.add_option('-n', '--train')
    parser.add_option('-r', '--trainLabel')
    parser.add_option('-v', '--validation')
    parser.add_option('-a', '--validationLabel')
    parser.add_option('-k', '--k')
    parser.add_option('-t', '--test')
    options, junk = parser.parse_args(args)
    return options


def doCommand(options):
    if options.k is None or options.train is None or options.trainLabel is None:
        print 'Not enough options'
        return
    if options.test is None:
        validate(options.train, options.trainLabel, options.validation, options.validationLabel, int(options.k), output=True)
    else:
        test(options.train, options.trainLabel, options.test, int(options.k))


if __name__ == '__main__':
    doCommand(parseCommand(sys.argv[1:]))

