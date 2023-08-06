#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from collections import defaultdict
class History:

    def __init__(self):
        self._history_log = []

    def update(self, history):
        self._history_log.append(history)

    def get_full_history(self):
        full_history = defaultdict(list)
        for history in self._history_log:
            for k, v in history.history.items():
                full_history[k].extend(v)

        return full_history

    def show(self, train='acc', validation=None):
        train_history = self.get_full_history()
        if validation is None:
            validation = 'val_' + train
        plt.plot(train_history[train], label='train')
        plt.plot(train_history[validation], label='validation')
        plt.title('Train history')
        plt.ylabel(train)
        plt.xlabel('Epoch')
        plt.legend(loc='best')
        plt.show()
