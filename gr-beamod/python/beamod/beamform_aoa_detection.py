#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2026 DanielSiboni.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr

class beamform_aoa_detection(gr.sync_block):
    """
    docstring for block beamform_aoa_detection
    """
    def __init__(self, freq=2.4e9):
        gr.sync_block.__init__(self,
            name="beamform_aoa_detection",
            in_sig=[np.complex64, np.complex64],
            out_sig=[np.float32, ])
        self.c = 299792458
        self.freq = freq
        self.lambda_ = self.c / freq
        self.d = self.lambda_ / 2
        self.sig1 = np.array([])
        self.sig2 = np.array([])
        self.theta = 0


    def work(self, input_items, output_items):
        in0 = input_items[0]
        in1 = input_items[1]

        out = output_items[0]

        if len(self.sig1) < 1000 and len(self.sig2) < 1000:
            self.sig1 = np.hstack((in0, self.sig1))
            self.sig2 = np.hstack((in1, self.sig2))
            out[:] = self.theta
            return len(output_items[0])

        P1 = np.sum
        
        cross = self.sig1 * np.conj(self.sig2)
        phase = np.angle(cross)

        phase_mean = np.mean(phase)

        self.theta = np.arcsin((phase_mean * self.lambda_) / (2*np.pi*self.d))

        self.sig1 = np.array([])
        self.sig2 = np.array([])

        out[:] = self.theta
        return len(output_items[0])
