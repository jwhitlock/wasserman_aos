#! /usr/bin/env python3
"""
Suppose we toss a fair coin until we get exactly two heads. What is the
probability that exactly k tosses are required?
"""

from collections import Counter
from random import choice

from prettytable import PrettyTable


def sample_k():
    '''Return flips to get exactly 2 heads'''
    head_count = 0
    count = 0
    while head_count < 2:
        count += 1
        if choice(['H', 'T']) == 'H':
            head_count += 1
    return count


def run_trials(number):
    '''Return count of flips to get to 2 heads over (number) trials'''
    counts = Counter()
    for i in range(number):
        counts[sample_k()] += 1
    return counts


def predict_pk(k, number):
    '''Predict the number of events for a given flip count.'''
    return (number * float(k - 1)) / float(2 ** k)


def show_error(number):
    '''Run the experiment, compare to prediction'''
    trials = run_trials(number)
    max_k = max(trials.keys())
    table = PrettyTable(('k', 'Predicted', 'Actual', 'Error%'))
    table.float_format = '0.1'
    table.align = 'r'
    for i in range(1, max_k+1):
        predict = predict_pk(i, number)
        actual = trials[i]
        if predict:
            error = abs(predict - actual) / predict
        else:
            error = abs(predict - actual)
        table.add_row((i, predict, actual, 100.0 * error))
    print('In %d trials:' % number)
    print(table)


show_error(1000000)
