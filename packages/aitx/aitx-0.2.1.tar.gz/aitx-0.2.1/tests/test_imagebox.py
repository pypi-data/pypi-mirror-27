#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
test_imagebox
----------------------------------

Tests for `imagebox` module.
"""

import unittest
import numpy as np

from aitx.imagebox import ImageBox


def _create_image(grayscale=True, shape=(10, 10)):
    if grayscale:
        size = shape[0] * shape[1]
        gray = np.random.randint(150, 256, shape).astype('float32')
        gray[2:8, 2:8] = 128
        gray[4:6, 4:6] = 0
        return gray
    else:
        shape = (*shape[:2], 3)
        size = shape[0] * shape[1] * 3
        rgb = np.random.randint(150, 256, shape).astype('float32')
        rgb[2:8, 2:8, :] = 128.0
        rgb[4:6, 4:6, :] = 0.0
        return rgb

def create_images(size=10, **kwarg):
    raw_images = [_create_image(**kwarg) for _ in range(size)]
    shape = raw_images[0].shape
    new_shape = (1, *shape)
    images = np.concatenate([i.reshape(new_shape) for i in raw_images])
    return images


class TestImagebox(unittest.TestCase):

    def setUp(self):
        self.size = 10
        self.shape = (10, 10)
        self.gray = create_images(self.size)
        self.rgb = create_images(self.size, grayscale=False)
        self.normal_gray = (self.gray / 255).reshape(10, 10, 10, 1)
        self.normal_rgb = self.rgb / 255
        self.labels = np.array([0, 1]*int(self.size/2))
        self.label_dict={0: False, 1: True}

    def test_init(self):
        # gray
        ib = ImageBox(self.gray, self.labels, self.label_dict)
        self.assertTrue(np.all(ib.grayscale==self.gray))
        self.assertEqual(ib.rgb, None)
        self.assertEqual(ib.image4D.shape, (self.size, *self.shape, 1))
        self.assertTrue(np.all(ib.normalize==self.normal_gray))

        # rgb
        ib = ImageBox(self.rgb, self.labels, self.label_dict)
        self.assertEqual(ib.grayscale, None)
        self.assertTrue(np.all(ib.rgb==self.rgb))
        self.assertEqual(ib.image4D.shape, (self.size, *self.shape, 3))
        self.assertTrue(np.all(ib.normalize==self.normal_rgb))

        # normal gray
        ib = ImageBox(self.normal_gray, self.labels, self.label_dict)
        self.assertTrue(np.all(ib.grayscale==self.normal_gray))
        self.assertEqual(ib.rgb, None)
        self.assertEqual(ib.image4D.shape, (self.size, *self.shape, 1))
        self.assertTrue(np.all(ib.normalize==self.normal_gray))

        # normal rgb
        ib = ImageBox(self.normal_rgb, self.labels, self.label_dict)
        self.assertEqual(ib.grayscale, None)
        self.assertTrue(np.all(ib.rgb==self.normal_rgb))
        self.assertEqual(ib.image4D.shape, (self.size, *self.shape, 3))
        self.assertTrue(np.all(ib.normalize==self.normal_rgb))

    def tearDown(self):
        pass
