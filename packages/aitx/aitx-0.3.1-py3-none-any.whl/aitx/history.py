#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.patches as patches

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

    def plot(self, train='acc', validation=None):
        if validation is None:
            validation = 'val_' + train

        epoch_left = 0
        for i, history_obj in enumerate(self._history_log):
            train_history = history_obj.history
            epochs = len(train_history[train])
            epoch_right = epoch_left + epochs
            if i % 2 == 1:
                axes = plt.gca()
                axes.add_patch(patches.Rectangle(
                                (epoch_left+0.5, 0),   # (x,y)
                                epochs,         # width
                                1.5,          # height
                                color='#f6f6f6'
                            ))
            epoch_left = epoch_right

        full_history = self.get_full_history()
        full_epochs = len(full_history[train])
        if self.human_accuracy is not None:
            plt.plot([0, full_epochs], [self.human_accuracy, self.human_accuracy], linestyle='--', color='gray', label='human')
        plt.plot(range(1, full_epochs+1), full_history[train], label='train')
        plt.plot(range(1, full_epochs+1), full_history[validation], label='validation')

        plt.title('Train history')
        plt.ylabel(train)
        plt.xlabel('Epoch')
        plt.xticks(range(0, full_epochs+1))
        plt.legend(loc='best')
        axes.set_xlim([0.5, full_epochs+0.5])
        axes.set_ylim([0, 1.1])
        plt.show()

    def show(self, train='acc', validation=None):
        self.plot(train, validation)

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
