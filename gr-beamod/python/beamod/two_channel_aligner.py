#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2026 Dolev Dilmoney.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr

class two_channel_aligner(gr.sync_block):
    def __init__(self, sample_rate=5e6, cal_duration_sec=3.0):
        gr.sync_block.__init__(self,
            name="two_channel_aligner",
            in_sig=[np.complex64, np.complex64],
            out_sig=[np.complex64, np.complex64])

        self.sample_rate = sample_rate
        self.cal_limit = int(sample_rate * cal_duration_sec)
        self.samples_processed = 0
        
        # gather data for the averge
        self.sum_x0_x1_conj = 0j
        self.sum_abs_x1_sq = 0.0
        
        self.cal_factor = 1.0 + 0j
        self.is_calibrated = False

    def work(self, input_items, output_items):
        in0 = input_items[0]
        in1 = input_items[1]
        n_samples = len(in0)

        # caliberating
        if self.samples_processed < self.cal_limit:
            if self.samples_processed == 0:
                print("--- Calibration Started: Keep Jammer at 0 degrees ---")
            
            # collcete data
            self.sum_x0_x1_conj += np.sum(in0 * np.conj(in1))
            self.sum_abs_x1_sq += np.sum(np.abs(in1)**2)
            
            self.samples_processed += n_samples
            
            # bypeass
            output_items[0][:] = in0
            output_items[1][:] = in1
            
            # check if we finish caliberating
            if self.samples_processed >= self.cal_limit:
                self.cal_factor = self.sum_x0_x1_conj / (self.sum_abs_x1_sq + 1e-12)
                self.is_calibrated = True
                print(f"--- Calibration Complete! ---")
                print(f"Correction Factor calculated: {self.cal_factor}")
                print(f"Phase Correction (deg): {np.degrees(np.angle(self.cal_factor))}")
                print(f"Amplitude Correction: {np.abs(self.cal_factor)}")

        # after caliberation
        else:
            # channel zero stay the same
            output_items[0][:] = in0
            # channel one get fixed
            output_items[1][:] = in1 * self.cal_factor

        return n_samples