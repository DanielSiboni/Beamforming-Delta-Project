#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import beamod
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import numpy as np
import sip



class first_try_pa(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "first_try_pa")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.wavelength = wavelength = 99792458.0 / 2.4e9
        self.jammer_angle = jammer_angle = np.radians(30)
        self.d_x = d_x = wavelength / 2
        self.samp_rate = samp_rate = 2e6
        self.pilot_offset = pilot_offset = 500e3
        self.phase_shift = phase_shift = 2 * np.pi * (d_x / wavelength) * np.sin(jammer_angle)

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            2,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.freq_xlating_fir_filter_xxx_0_0 = filter.freq_xlating_fir_filter_ccc(1, firdes.low_pass(1.0, samp_rate, 10e3, 2e3), (-pilot_offset), samp_rate)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, firdes.low_pass(1.0, samp_rate, 10e3, 2e3), (-pilot_offset), samp_rate)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_delay_0_2 = blocks.delay(gr.sizeof_gr_complex*1, (int(3 * phase_shift)))
        self.blocks_delay_0_1 = blocks.delay(gr.sizeof_gr_complex*1, (int(2 * phase_shift)))
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_gr_complex*1, (int(1 * phase_shift)))
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, (int(-0 * phase_shift)))
        self.blocks_add_xx_0_2 = blocks.add_vcc(1)
        self.blocks_add_xx_0_1 = blocks.add_vcc(1)
        self.blocks_add_xx_0_0 = blocks.add_vcc(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.beamod_pilot_sync_0 = beamod.pilot_sync()
        self.beamod_mvdr_beamformer_0 = beamod.mvdr_beamformer(0.0, [0, d_x, 2*d_x, 3*d_x], 2.4e9, (512 * 10))
        self.analog_sig_source_x_0_3_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 1, 1, 0, 0)
        self.analog_sig_source_x_0_3 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 500e3, 1, 0, 0)
        self.analog_sig_source_x_0_2 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 10e3, 1, 0, 0)
        self.analog_sig_source_x_0_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 10e3, 1, 0, 0)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 10e3, 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 10e3, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.analog_sig_source_x_0_1, 0), (self.blocks_delay_0_1, 0))
        self.connect((self.analog_sig_source_x_0_2, 0), (self.blocks_delay_0_2, 0))
        self.connect((self.analog_sig_source_x_0_3, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.analog_sig_source_x_0_3, 0), (self.blocks_add_xx_0_0, 0))
        self.connect((self.analog_sig_source_x_0_3, 0), (self.blocks_add_xx_0_1, 0))
        self.connect((self.analog_sig_source_x_0_3, 0), (self.blocks_add_xx_0_2, 0))
        self.connect((self.analog_sig_source_x_0_3_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_0_3_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.beamod_mvdr_beamformer_0, 0), (self.qtgui_freq_sink_x_0, 1))
        self.connect((self.beamod_pilot_sync_0, 0), (self.beamod_mvdr_beamformer_0, 2))
        self.connect((self.beamod_pilot_sync_0, 1), (self.beamod_mvdr_beamformer_0, 3))
        self.connect((self.blocks_add_xx_0, 0), (self.beamod_mvdr_beamformer_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_add_xx_0_0, 0), (self.beamod_mvdr_beamformer_0, 1))
        self.connect((self.blocks_add_xx_0_1, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.blocks_add_xx_0_2, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_delay_0_0, 0), (self.blocks_add_xx_0_0, 1))
        self.connect((self.blocks_delay_0_1, 0), (self.blocks_add_xx_0_1, 1))
        self.connect((self.blocks_delay_0_2, 0), (self.blocks_add_xx_0_2, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.beamod_pilot_sync_0, 1))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.beamod_pilot_sync_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.freq_xlating_fir_filter_xxx_0_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.beamod_pilot_sync_0, 2))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.beamod_pilot_sync_0, 3))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "first_try_pa")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_wavelength(self):
        return self.wavelength

    def set_wavelength(self, wavelength):
        self.wavelength = wavelength
        self.set_d_x(self.wavelength / 2)
        self.set_phase_shift(2 * np.pi * (self.d_x / self.wavelength) * np.sin(self.jammer_angle))

    def get_jammer_angle(self):
        return self.jammer_angle

    def set_jammer_angle(self, jammer_angle):
        self.jammer_angle = jammer_angle
        self.set_phase_shift(2 * np.pi * (self.d_x / self.wavelength) * np.sin(self.jammer_angle))

    def get_d_x(self):
        return self.d_x

    def set_d_x(self, d_x):
        self.d_x = d_x
        self.set_phase_shift(2 * np.pi * (self.d_x / self.wavelength) * np.sin(self.jammer_angle))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_1.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_2.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_3.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_3_0.set_sampling_freq(self.samp_rate)
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.low_pass(1.0, self.samp_rate, 10e3, 2e3))
        self.freq_xlating_fir_filter_xxx_0_0.set_taps(firdes.low_pass(1.0, self.samp_rate, 10e3, 2e3))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_pilot_offset(self):
        return self.pilot_offset

    def set_pilot_offset(self, pilot_offset):
        self.pilot_offset = pilot_offset
        self.freq_xlating_fir_filter_xxx_0.set_center_freq((-self.pilot_offset))
        self.freq_xlating_fir_filter_xxx_0_0.set_center_freq((-self.pilot_offset))

    def get_phase_shift(self):
        return self.phase_shift

    def set_phase_shift(self, phase_shift):
        self.phase_shift = phase_shift
        self.blocks_delay_0.set_dly(int((int(-0 * self.phase_shift))))
        self.blocks_delay_0_0.set_dly(int((int(1 * self.phase_shift))))
        self.blocks_delay_0_1.set_dly(int((int(2 * self.phase_shift))))
        self.blocks_delay_0_2.set_dly(int((int(3 * self.phase_shift))))




def main(top_block_cls=first_try_pa, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
