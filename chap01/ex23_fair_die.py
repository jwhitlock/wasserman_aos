#! /usr/bin/env python3
"""
Toss a fair die.
Event A = {2,4,6}, B = {1,2,3,4}.
So P(A) = 1/2, P(B) = 2/3, and P(AB)= 1/3 (so A and B are independent).

Verify that P^(AB)=P^(A) P^(B).
Pick A and B that are not independent, verify P^(AB) != P^(A) P^(B).

"""

from collections import Counter
from random import randint

from prettytable import PrettyTable


def sample_die():
    """Roll a fair die."""
    return randint(1, 6)


def run_trials(a_set, b_set, number):
    """Count P^ for A, B, and AB."""
    counts = Counter()
    for n in range(number):
        roll = sample_die()
        in_a = roll in a_set
        in_b = roll in b_set
        if in_a:
            counts['a'] += 1
        if in_b:
            counts['b'] += 1
        if in_a and in_b:
            counts['ab'] += 1
    return counts


def predict(a_set, b_set, number):
    """Predict P^ for A, B, and AB."""
    return {
        'a': number * (len(a_set) / 6.0),
        'b': number * (len(b_set) / 6.0),
        'ab': number * (len(a_set & b_set) / 6.0),
    }


def show_error(a_set, b_set, number):
    '''Run the experiment, compare to prediction'''
    trials = run_trials(a_set, b_set, number)
    predicted_count = predict(a_set, b_set, number)
    keys = ('a', 'b', 'ab')
    table = PrettyTable(('Event', 'Predicted', 'P%', 'Actual', 'A%', 'Error%'))
    table.float_format = '0.1'
    table.align = 'r'
    for key in keys:
        actual = trials[key]
        ap = actual / float(number)
        predicted = predicted_count[key]
        pp = predicted / float(number)
        if predicted:
            error = abs(predicted - actual) / predicted
        else:
            error = abs(predicted - actual)
        table.add_row((key, predicted, 100 * pp, actual, 100 * ap,
                       100.0 * error))
    print('In %d trials:' % number)
    print(table)
    pa = trials['a'] / float(number)
    pb = trials['b'] / float(number)
    pab = trials['ab'] / float(number)
    print("P^(A)*P^(B) = %0.1f" % (100 * (pa * pb)))
    print("     P^(AB) = %0.1f" % (100 * pab))


number = 100000
print("Independent Events")
a_set = {2, 4, 6}
b_set = {1, 2, 3, 4}
show_error(a_set, b_set, number)

print()
print("Non-Independent Events")
a_set = {2, 4, 6}
b_set = {4, 6}
show_error(a_set, b_set, number)
