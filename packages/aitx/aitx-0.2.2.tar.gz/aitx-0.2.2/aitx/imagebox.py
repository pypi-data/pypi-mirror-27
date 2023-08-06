#!/usr/bin/env python
# -*- coding: utf-8 -*-

from keras.utils import np_utils
import numpy as np
from functools import reduce

class ImageBox:
    def __init__(self, image, labels=None, label_dict=None, prediction=None):
        """
        Grayscale image in 3D shape: (batch, width, height)
        Colored image in 4D shape: (batch, width, height, channel)
        labels in 1D shape: (batch,) or one_hot_label in 2D shape: (batch, label)
        """
        if len(image.shape) == 3 or image.shape[3] == 1:
            self.grayscale = image
            self.rgb = None
            self.image4D = image.reshape((*image.shape[:3], 1))
        else:
            self.rgb = image
            self.grayscale = None
            self.image4D = image
        self.float32 = self.image4D.astype('float32')
        if np.max(image) > 1:
            self.normalize = self.float32 / 255
        else:
            self.normalize = self.float32

        if labels is not None:
            if len(labels.shape) == 1:
                self.labels = labels
                self.one_hot = np_utils.to_categorical(labels).astype('float32')
            else: # labels in 2D shape
                self.one_hot = labels
                self.labels = np.array([np.where(r==1)[0][0] for r in labels]).astype('int32')
        else:
            self.labels = None

        if label_dict is None:
            self.label_dict = {}
        else:
            self.label_dict = label_dict
        self.prediction = prediction


    def show(self, idx=None, prediction=None):
        """
        Display the example images and labels
        """
        import matplotlib
        from matplotlib import pyplot as plt

        def ceildiv(a, b):
            return -(-a // b)

        if idx is None:
            idx = list(range(min(10, self.image4D.shape[0])))
        rownumber = ceildiv(len(idx), 5)

        if prediction is not None:
            self.prediction = prediction

        fig = plt.figure()
        fig.set_size_inches(12, 2.8 * rownumber)

        for n, i in enumerate(idx):
            ax = plt.subplot(rownumber, 5, n+1)
            img_to_show = np.clip(self.normalize[i], 0.0, 1.0)
            if img_to_show.shape[2] == 1:
                img_to_show = img_to_show.reshape(img_to_show.shape[0],
                                                  img_to_show.shape[1])
            ax.imshow(img_to_show, cmap='binary')

            title_items = ['#', str(i), ' ']
            if self.labels is not None:
                title_items.append('label=')
                title_items.append(self.label_dict.get(self.labels[i], str(self.labels[i])))
            if prediction is not None:
                title_items.append([' => ',
                                label_dict.get(prediction[i], prediction[i])])
            title = ''.join([str(it) for it in title_items])
            ax.set_title(title, fontsize=10)
            ax.set_xticks([])
            ax.set_yticks([])
        plt.show()

    def to_rgb(self):
        if self.rgb is None:
            self.rgb = np.tile(self.image4D, (1, 1, 1, 3))
        return self.rgb
