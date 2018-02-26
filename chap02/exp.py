#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt


def exp_beta_pdf(beta, x):
    '''Calculate the exponential distribution Exp(beta) PDF'''
    gamma = 1.0 / beta
    curve = np.exp(-gamma * x)
    return gamma * curve


def exp_beta_cdf(beta, x):
    '''Calculate the exponential distribution Exp(beta) CDF'''
    gamma = 1.0 / beta
    curve = np.exp(-gamma * x)
    return 1 - curve


def plot_exp_beta(beta):
    x = np.linspace(0, 10, 100)
    pdf = exp_beta_pdf(beta, x)
    cdf = exp_beta_cdf(beta, x)
    ints = np.arange(11)
    pdf_ints = exp_beta_pdf(beta, ints)
    cdf_ints = exp_beta_cdf(beta, ints)

    plt.subplot(211)
    plt.plot(x, pdf)
    plt.title('Exp(%0.1f) Probability Density Function (PDF)' % beta)
    for xy in zip(ints, pdf_ints):
        plt.annotate('%0.2f' % xy[1], xy=xy, textcoords='data')

    plt.subplot(212)
    plt.plot(x, cdf)
    plt.title('Exp(%0.1f) Cummulative Distribution Function (CDF)' % beta)
    for xy in zip(ints, cdf_ints):
        plt.annotate('%0.2f' % xy[1], xy=xy, textcoords='data')

    plt.show()


beta = 2
plot_exp_beta(beta)
