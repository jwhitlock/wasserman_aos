#! /usr/bin/env python
"""
Chance of blue eyes is 1/4, and independent. Consider a family of 3 kids:

1. If one kid has blue eyes, what is probability that at least one other does?
2. If youngest has blue eyes, what is probability that at least one other does?
"""

from collections import Counter
from random import choice

from prettytable import PrettyTable


def sample_eyes():
    '''Return True if kid has blue eyes.'''
    return choice((True, False, False, False))


def sample_kids():
    '''Return kids, True if has blue eyes'''
    return [sample_eyes() for _ in range(3)]


def at_least_one():
    '''Return True if two or three in family'''
    while True:
        kids = sample_kids()
        if True in kids:
            return kids.count(True) > 1


def youngest_plus_one():
    '''Return True if youngest and at least one more'''
    while True:
        kids = sample_kids()
        if kids[0]:
            return kids.count(True) > 1


def run_trials(number):
    '''Return count of flips to get to 2 heads over (number) trials'''
    counts = Counter()
    for i in xrange(number):
        if at_least_one():
            counts['at_least_one'] += 1
        if youngest_plus_one():
            counts['youngest_plus_one'] += 1
    return counts


def predict(event, number):
    '''Predict the number of events for a given flip count.'''
    factor = {
        'at_least_one': 10.0 / 37.0,
        'youngest_plus_one': 7.0 / 16.0,
    }
    return number * factor[event]


def show_error(number):
    '''Run the experiment, compare to prediction'''
    trials = run_trials(number)
    table = PrettyTable(('Event', 'Predicted', 'Actual', 'Error%'))
    table.float_format = '0.1'
    table.align = 'r'
    for event in sorted(trials.keys()):
        predicted = predict(event, number)
        actual = trials[event]
        if predicted:
            error = abs(predicted - actual) / predicted
        else:
            error = abs(predicted - actual)
        table.add_row((event, predicted, actual, 100.0 * error))
    print('In %d trials:' % number)
    print(table)


show_error(1000000)
