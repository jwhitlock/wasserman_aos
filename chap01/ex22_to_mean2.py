#! /usr/bin/env python3
"""
Flip a coin that has heads 30% 10, 100, and 1000 time.
Repeat and average the results. Does the averages converge
toward n * p?
"""

from random import random

from prettytable import PrettyTable


def flip_coin(chance_of_heads):
    return random() <= chance_of_heads


def run_trial(flips, chance_of_heads):
    '''Flip <flips> times, return heads'''
    heads = 0
    for n in range(flips):
        if flip_coin(chance_of_heads):
            heads += 1
    return heads


def repeat_trials(trials, flips, chance_of_heads):
    '''Repeat <trials> trials.'''
    result = []
    for n in range(trials):
        result.append(run_trial(flips, chance_of_heads))
    return result


def predict_heads(flips, chance_of_heads):
    return flips * chance_of_heads


def show_results(chance):
    flips = [10, 100, 1000]
    trials = 1000
    results = [repeat_trials(trials, flip, chance) for flip in flips]
    total = [0] * 3
    table = PrettyTable(['Trials'] +
                        ['n=%d' % n for n in flips] +
                        ['n=%d (Avg)' % n for n in flips])
    table.float_format = '0.1'
    table.align = 'r'
    table.add_row(['(n*p)'] +
                  [int(predict_heads(n, chance)) for n in flips] +
                  [predict_heads(n, chance) for n in flips])
    for num, row in enumerate(zip(*results)):
        total = [t + n for t, n in zip(total, row)]
        average = [t / float(num + 1) for t in total]
        str_num = str(num + 1)
        if str_num[1:] == "0" * (len(str_num) - 1):
            table.add_row([num + 1] + list(row) + average)
    print(table)


show_results(0.3)
