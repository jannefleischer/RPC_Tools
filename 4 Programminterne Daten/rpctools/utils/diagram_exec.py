from argparse import ArgumentParser
import matplotlib.pyplot as plt
from pickle import load

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-f', '--file', dest='file',
                        help='File with pickled plots')
    options = parser.parse_args()
    with open(options.file, 'r') as f:
        figure = load(f)
    plt.show()
    