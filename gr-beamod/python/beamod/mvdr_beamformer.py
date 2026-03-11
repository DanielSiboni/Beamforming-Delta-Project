#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2026 DanielSiboni.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy as np
from gnuradio import gr

class mvdr_beamformer(gr.sync_block):
    """
    Generic MVDR Beamformer Block for N antennas.
    """
    # שים לב: המיקומים צריכים להיות במטרים! למשל 6.5 ס"מ יהיה 0.065
    def __init__(self, target_angle=0.0, ant_positions=[0.0, 0.065], freq=2.4e9, snapshots=512):
        
        # זיהוי אוטומטי של מספר האנטנות
        self.num_antennas = len(ant_positions)
        
        # יצירת כניסות דינמיות בהתאם למספר האנטנות
        gr.sync_block.__init__(self,
            name="MVDR Beamformer N-Elements",
            in_sig=[np.complex64] * self.num_antennas,
            out_sig=[np.complex64])

        # פרמטרים פיזיקליים
        self.target_rad = np.radians(target_angle)
        self.ant_positions = np.array(ant_positions)
        self.freq = freq
        
        # תוקן: מהירות האור במטרים לשנייה
        self.wavelength = 299792458.0 / freq 
        self.snapshots = snapshots
        
        self.a_s = self._calculate_steering_vector()

        # באפר ומשקולות דינמיים
        self.buffer = np.zeros((self.num_antennas, 0), dtype=np.complex64)
        self.weights = self.a_s.flatten() / self.num_antennas

    def _calculate_steering_vector(self):
        # חישוב וקטור גנרי לכל מספר של אנטנות
        phases = 2 * np.pi * self.ant_positions * np.sin(self.target_rad) / self.wavelength
        return np.exp(-1j * phases).reshape(self.num_antennas, 1)

    def work(self, input_items, output_items):
        n_samples = len(input_items[0])
        
        # הפיכת כל הכניסות למטריצה אחת של N שורות
        in_data = np.array(input_items, dtype=np.complex64)

        # עדכון באפר
        self.buffer = np.hstack((self.buffer, in_data))

        # חישוב MVDR
        if self.buffer.shape[1] >= self.snapshots:
            X_snap = self.buffer[:, :self.snapshots]
            
            R = np.dot(X_snap, X_snap.conj().T) / self.snapshots
            signal_power = np.trace(R).real / self.num_antennas
            R += np.eye(self.num_antennas) * ((signal_power * 1e-6) + 1e-12)
            
            try:
                R_inv = np.linalg.inv(R)
                num = np.dot(R_inv, self.a_s)
                den = np.dot(self.a_s.conj().T, num)
                self.weights = (num / den).flatten()
            except np.linalg.LinAlgError:
                pass
            
            self.buffer = self.buffer[:, self.snapshots:]

        # יישום המשקולות על כל הדגימות (עובד ל-N אנטנות בבת אחת)
        # מכפילים כל שורה באנטנה במשקולת הצמודה שלה, ומסכמים
        output_items[0][:] = np.dot(self.weights.conj(), in_data)

        return n_samples