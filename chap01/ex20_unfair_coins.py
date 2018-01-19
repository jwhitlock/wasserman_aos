#! /usr/bin/env python3
"""
You have five coins, with these chances of heads:

1: 0%
2: 25%
3: 50%:
4: 75%
5: 100%

Pick a coin at random, keep flipping

1. If you get heads, what is the chance it is coin X?
2. If you get heads on flip 1, what is the chance of heads on flip 2?
3. If the first head is on flip 5, what is the chance it is coin X?
3a. What is the chance of first heads on flip 5?
"""

from collections import Counter
from random import choice, randint

from prettytable import PrettyTable

coins = dict((
    (1, (False, False, False, False)),
    (2, (False, False, False, True)),
    (3, (False, False, True, True)),
    (4, (False, True, True, True)),
    (5, (True, True, True, True)),
))


def sample_coin():
    '''Return coin #, True if heads'''
    coin = randint(1, 5)
    return coin, flip_coin(coin)


def flip_coin(coin):
    return choice(coins[coin])


def sample_1_head():
    '''Return coin # if result was heads.'''


def predict_1_coin_if_heads(coin, head_total):
    '''Predict times it was coin X out of all head events.'''
    return ((coin - 1) * head_total) / 10.0


def predict_heads(coin, number):
    '''Predict times that coin would be heads.'''
    heads = coins[coin].count(True)
    total = len(coins[coin])
    percent = float(heads) / float(total)
    return percent * number


def predict_heads5_from_universe(coin, number):
    '''Predict times that coin would first be heads on flip 5.'''
    heads = coins[coin].count(True)
    tails = coins[coin].count(False)
    total = len(coins[coin])
    assert heads + tails == total
    percent = float(tails * tails * tails * tails * heads) / float(total ** 5)
    return percent * number / 5.0


def predict_coin_from_head5(coin, head5_total):
    '''Predict times that coin would first be heads on flip 5.'''
    numerator = {
        1: 0,
        2: 81,
        3: 31,
        4: 3,
        5: 0.
    }
    percent = float(numerator[coin]) / float(sum(numerator.values()))
    return percent * head5_total


def run_trials(number):
    '''Flip Return count of flips to get to 2 heads over (number) trials'''
    counts = {
        'picked': Counter(),
        'heads1': Counter(),
        'heads2': Counter(),
        'heads5': Counter(),
    }
    for i in range(number):
        coin, heads = sample_coin()
        counts['picked'][coin] += 1
        if heads:
            counts['heads1'][coin] += 1
            heads2 = flip_coin(coin)
            if heads2:
                counts['heads2'][coin] += 1
        else:
            tail_count = 1
            while (not heads) and tail_count < 5:
                heads = flip_coin(coin)
                if not heads:
                    tail_count += 1
            if heads and tail_count == 4:
                counts['heads5'][coin] += 1
    return counts


def error_percent(predicted, actual):
    if predicted:
        error = abs(predicted - actual) / predicted
    else:
        error = abs(predicted - actual)
    return error * 100.0


def show_error(number):
    '''Run the experiment, compare to prediction'''
    trials = run_trials(number)
    heads1_total = sum(trials['heads1'].values())
    heads2_total = sum(trials['heads2'].values())
    heads5_total = sum(trials['heads5'].values())
    table = PrettyTable(('Coin', 'Picked',
                         'Heads Pred', 'H Actual', 'H Err%',
                         '2nd H Pred', '2H Act', '2H Err%',
                         '5th H Pred U', '5th H Pred B', '5H Act', '5HU Err%',
                         '5HB Err%'))
    table.float_format = '0.1'
    table.align = 'r'
    for coin in range(1, 6):
        picked = trials['picked'][coin]
        heads1_pred = predict_1_coin_if_heads(coin, heads1_total)
        heads1_actual = trials['heads1'][coin]
        heads1_error = error_percent(heads1_pred, heads1_actual)
        heads2_pred = predict_heads(coin, heads1_actual)
        heads2_actual = trials['heads2'][coin]
        heads2_error = error_percent(heads2_pred, heads2_actual)
        heads5_predu = predict_heads5_from_universe(coin, number)
        heads5_predb = predict_coin_from_head5(coin, heads5_total)
        heads5_actual = trials['heads5'][coin]
        heads5u_error = error_percent(heads5_predu, heads5_actual)
        heads5b_error = error_percent(heads5_predb, heads5_actual)
        table.add_row((coin, picked,
                       heads1_pred, heads1_actual, heads1_error,
                       heads2_pred, heads2_actual, heads2_error,
                       heads5_predu, heads5_predb, heads5_actual,
                       heads5u_error, heads5b_error))
    print('In %d trials:' % number)
    print(table)

    hah_pred = 3.0 / 4.0
    hah_actual = float(heads2_total) / float(heads1_total)
    hah_error = error_percent(hah_pred, hah_actual)
    print('Chance of heads after first head')
    print('   Actual: %0.1f%% (%d of %d)'
          % (hah_actual * 100.0, heads2_total, heads1_total))
    print('Predicted: %0.1f%% (%d of %d) (error %0.1f%%)'
          % (hah_pred * 100.0, int(hah_pred * heads1_total), heads1_total,
             hah_error))

    h5_pred = 106.0 / (5.0 * 1024.0)
    h5_actual = float(heads5_total) / float(number)
    h5_error = error_percent(h5_pred, h5_actual)
    print('Chance that 5th flip is heads')
    print('   Actual: %0.1f%% (%d of %d)'
          % (h5_actual * 100.0, heads5_total, number))
    print('Predicted: %0.1f%% (%d of %d) (error %0.1f%%)'
          % (h5_pred * 100.0, int(h5_pred * heads5_total), heads5_total,
             h5_error))


show_error(1024 * 1024 * 8)
