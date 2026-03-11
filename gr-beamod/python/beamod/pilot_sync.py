#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from gnuradio import gr

class pilot_sync(gr.sync_block):
    """
    Dynamically corrects phase drift between two independent USRPs 
    using isolated pilot tones.
    """
    def __init__(self):
        gr.sync_block.__init__(
            self,
            name="Pilot Tone Phase Synchronizer",
            # We need 4 inputs:
            # in[0]: Raw Data - USRP B, Ant 3 (Drifting)
            # in[1]: Raw Data - USRP B, Ant 4 (Drifting)
            # in[2]: Isolated Pilot Tone - USRP A (The "Master" Reference)
            # in[3]: Isolated Pilot Tone - USRP B (The "Slave" Pilot)
            in_sig=[np.complex64, np.complex64, np.complex64, np.complex64],
            
            # We output the 2 phase-corrected streams for USRP B
            out_sig=[np.complex64, np.complex64]
        )

    def work(self, input_items, output_items):
        raw_b3 = input_items[0]
        raw_b4 = input_items[1]
        pilot_a = input_items[2]
        pilot_b = input_items[3]

        # 1. Calculate the instantaneous complex phase difference
        # Multiplying by the conjugate gives us the angular difference
        phase_diff = pilot_a * np.conj(pilot_b)
        
        # 2. Normalize to get ONLY the phase rotation vector (magnitude = 1)
        mag = np.abs(phase_diff)
        # Prevent division by zero if the pilot drops out
        mag[mag == 0] = 1e-6 
        correction_vector = phase_diff / mag

        # 3. Apply the correction vector to the wideband data of USRP B
        # This mathematically locks USRP B's local oscillator to USRP A
        output_items[0][:] = raw_b3 * correction_vector
        output_items[1][:] = raw_b4 * correction_vector

        return len(input_items[0])