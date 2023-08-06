#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

def show_history(train='acc', validation=None):
    global train_history
    if validation is None:
        validation = 'val_' + train
    plt.plot(train_history.history[train], label='train')
    plt.plot(train_history.history[validation], label='validation')
    plt.title('Train history')
    plt.ylabel(train)
    plt.xlabel('Epoch')
    plt.legend(loc='best')
    plt.show()
