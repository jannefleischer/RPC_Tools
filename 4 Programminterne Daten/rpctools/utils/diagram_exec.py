from argparse import ArgumentParser
import matplotlib.pyplot as plt
from pickle import load
import os

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-f', '--file', dest='file',
                        help='File with pickled plots')
    options = parser.parse_args()
    with open(options.file, 'r') as f:
        figure = load(f)
    # workaround in older matplotlib versions, 
    # callbacks are not correctly pickled/unpickled
    figure.callbacks.callbacks = {}
    plt.show()
    os.remove(options.file)
    