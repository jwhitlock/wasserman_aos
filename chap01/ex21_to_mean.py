#! /usr/bin/env python3
"""
Flip a coin that has heads 30%, and 3%. What it the proportion of heads as
we filp the coin 1000 times?
"""

from random import random

import numpy as np
import matplotlib.pyplot as plt


def flip_coin(chance_of_heads):
    return random() <= chance_of_heads


def run_trials(number, chance_of_heads):
    '''Flip <number> times, return % heads after n trials'''
    heads = 0
    result = []
    for n in range(number):
        if flip_coin(chance_of_heads):
            heads += 1
        percent_heads = float(heads) / float(n + 1)
        result.append(percent_heads)
    return result


def plot_trial(number, chance1, chance2):
    result1 = run_trials(number, chance1)
    result2 = run_trials(number, chance2)
    points = np.arange(1, number+1)
    plt.plot(points, result1)
    plt.plot(points, np.ones(number) * chance1)
    plt.plot(points, result2)
    plt.plot(points, np.ones(number) * chance2)
    plt.title('Proportion of Heads, 30% and 3% coins')
    plt.ylabel('Percent Heads')
    plt.xlabel('Trials')
    plt.ylim(0, 1)
    plt.show()


plot_trial(1000, 0.3, 0.03)
