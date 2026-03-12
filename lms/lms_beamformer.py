#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from gnuradio import gr


class lms_beamformer(gr.sync_block):
    """
    LMS adaptive beamformer

    Inputs:
        0 -> antenna vector input, vlen = num_antennas
        1 -> desired/reference stream (complex64)

    Output:
        0 -> beamformed output stream (complex64)
    """

    def __init__(self, num_antennas=2, mu=0.001):
        self.num_antennas = int(num_antennas)
        self.mu = float(mu)

        if self.num_antennas < 2:
            raise ValueError("num_antennas must be at least 2")

        gr.sync_block.__init__(
            self,
            name="lms_beamformer",
            in_sig=[(numpy.complex64, self.num_antennas), numpy.complex64],
            out_sig=[numpy.complex64],
        )

        self.w = numpy.zeros(self.num_antennas, dtype=numpy.complex64)
        self.w[0] = 1.0 + 0.0j

    def work(self, input_items, output_items):
        antenna_vectors = input_items[0]   # shape: (noutput, num_antennas)
        d_stream = input_items[1]
        out = output_items[0]

        noutput = len(out)

        for n in range(noutput):
            x_n = antenna_vectors[n]
            y_n = numpy.vdot(self.w, x_n)
            e_n = d_stream[n] - y_n
            self.w += self.mu * x_n * numpy.conj(e_n)
            out[n] = y_n

        return noutput
