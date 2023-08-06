#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from collections import defaultdict
class History:

    def __init__(self):
        self._history_log = []
        self.human_accuracy = None

    def update(self, history):
        self._history_log.append(history)

    def set_human_accuracy(self, score):
        self.human_accuracy = score

    def get_full_history(self):
        full_history = defaultdict(list)
        for history in self._history_log:
            for k, v in history.history.items():
                full_history[k].extend(v)

        return full_history

    def show(self, train='acc', validation=None):
        train_history = self.get_full_history()
        epochs = len(train_history[train])
        if validation is None:
            validation = 'val_' + train
        if self.human_accuracy is not None:
            plt.plot([0, epochs], [self.human_accuracy, self.human_accuracy], linestyle='--', color='gray', label='human')
        plt.plot(train_history[train], label='train')
        plt.plot(train_history[validation], label='validation')

        plt.title('Train history')
        plt.ylabel(train)
        plt.xlabel('Epoch')
        plt.legend(loc='best')
        plt.show()

    def diagnosis(self, human_accuracy=None):
        if human_accuracy is not None:
            self.human_accuracy = human_accuracy
        if self.human_accuracy is None:
            print("Need human accuracy")
        full_history = self.get_full_history()
        hum_error = 1 - self.human_accuracy
        acc_error = 1 - full_history['acc'][-1]
        val_error = 1 - full_history['val_acc'][-1]
        template = "Human level error:\t{:.3f}\nTraining set error:\t{:.3f}\nDev/Test set error:\t{:.3f}"
        print(template.format(hum_error, acc_error, val_error))
        bias = max(0, acc_error - hum_error)
        variance = val_error - acc_error
        print('Avoidable bias:\t{:.3f}\nVariance:\t{:.3f}'.format(bias, variance))
        if bias >= variance:
            print('Recommend train on a larger model or more time.')
        else:
            print('{:->30}'.format(''))
            print('Recommend more regulation or dropout.')
