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
from PyQt5 import QtCore
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
        self.freq_wave = freq_wave = 50e3
        self.wavelength = wavelength = 99792458.0 / freq_wave
        self.jammer_angle_deg = jammer_angle_deg = 30
        self.jammer_angle = jammer_angle = np.radians(jammer_angle_deg)
        self.d_x = d_x = wavelength / 2
        self.samp_rate = samp_rate = 2e6
        self.pilot_offset = pilot_offset = 500e3
        self.phase_shift = phase_shift = 2 * np.pi * (d_x / wavelength) * np.sin(jammer_angle)
        self.c_light_speed = c_light_speed = 299792458.0
        self.P_noise = P_noise = 0

        ##################################################
        # Blocks
        ##################################################

        self._P_noise_range = qtgui.Range(0, 1, 0.1, 0, 200)
        self._P_noise_win = qtgui.RangeWidget(self._P_noise_range, self.set_P_noise, "'P_noise'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._P_noise_win)
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
        self._jammer_angle_deg_range = qtgui.Range(-90, 90, 1, 30, 200)
        self._jammer_angle_deg_win = qtgui.RangeWidget(self._jammer_angle_deg_range, self.set_jammer_angle_deg, "'jammer_angle_deg'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._jammer_angle_deg_win)
        self.freq_xlating_fir_filter_xxx_0_0 = filter.freq_xlating_fir_filter_ccc(1, firdes.low_pass(1.0, samp_rate, 10e3, 2e3), (-pilot_offset), samp_rate)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, firdes.low_pass(1.0, samp_rate, 10e3, 2e3), (-pilot_offset), samp_rate)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_1_0 = blocks.multiply_const_cc(10**(10/20))
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_cc(10**(10/20))
        self.blocks_multiply_const_vxx_0_0_0_0 = blocks.multiply_const_cc(np.exp(-1j * 3 * phase_shift))
        self.blocks_multiply_const_vxx_0_0_0 = blocks.multiply_const_cc(np.exp(-1j * 2 * phase_shift))
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_cc(np.exp(-1j * 1 * phase_shift))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(np.exp(-1j * 0 * phase_shift))
        self.blocks_add_xx_0_3_2 = blocks.add_vcc(1)
        self.blocks_add_xx_0_3_1 = blocks.add_vcc(1)
        self.blocks_add_xx_0_3_0 = blocks.add_vcc(1)
        self.blocks_add_xx_0_3 = blocks.add_vcc(1)
        self.blocks_add_xx_0_2 = blocks.add_vcc(1)
        self.blocks_add_xx_0_1 = blocks.add_vcc(1)
        self.blocks_add_xx_0_0 = blocks.add_vcc(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.beamod_pilot_sync_0 = beamod.pilot_sync()
        self.beamod_mvdr_beamformer_0 = beamod.mvdr_beamformer(0.0, [0, d_x, 2*d_x, 3*d_x], freq_wave, (512 * 10))
        self.band_pass_filter_0_0 = filter.fir_filter_ccf(
            1,
            firdes.band_pass(
                1,
                samp_rate,
                (0.9 * freq_wave),
                (1.1 * freq_wave),
                (0.01 * freq_wave),
                window.WIN_HAMMING,
                6.76))
        self.band_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.band_pass(
                1,
                samp_rate,
                (0.9 * freq_wave),
                (1.1 * freq_wave),
                (0.01 * freq_wave),
                window.WIN_HAMMING,
                6.76))
        self.analog_sig_source_x_0_3_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 1, 1, 0, 0)
        self.analog_sig_source_x_0_3 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, pilot_offset, 1, 0, 0)
        self.analog_sig_source_x_0_2 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, freq_wave, 1, 0, 0)
        self.analog_sig_source_x_0_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, freq_wave, 1, 0, 0)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, freq_wave, 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, freq_wave, 1, 0, 0)
        self.analog_noise_source_x_0_2 = analog.noise_source_c(analog.GR_GAUSSIAN, P_noise, 0)
        self.analog_noise_source_x_0_1 = analog.noise_source_c(analog.GR_GAUSSIAN, P_noise, 0)
        self.analog_noise_source_x_0_0 = analog.noise_source_c(analog.GR_GAUSSIAN, P_noise, 0)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, P_noise, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0_3, 1))
        self.connect((self.analog_noise_source_x_0_0, 0), (self.blocks_add_xx_0_3_0, 1))
        self.connect((self.analog_noise_source_x_0_1, 0), (self.blocks_add_xx_0_3_1, 1))
        self.connect((self.analog_noise_source_x_0_2, 0), (self.blocks_add_xx_0_3_2, 1))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_add_xx_0_3_0, 0))
        self.connect((self.analog_sig_source_x_0_1, 0), (self.blocks_add_xx_0_3_1, 0))
        self.connect((self.analog_sig_source_x_0_2, 0), (self.blocks_add_xx_0_3_2, 0))
        self.connect((self.analog_sig_source_x_0_3, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.analog_sig_source_x_0_3, 0), (self.blocks_add_xx_0_0, 0))
        self.connect((self.analog_sig_source_x_0_3, 0), (self.blocks_add_xx_0_1, 0))
        self.connect((self.analog_sig_source_x_0_3, 0), (self.blocks_add_xx_0_2, 0))
        self.connect((self.analog_sig_source_x_0_3_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_0_3_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.band_pass_filter_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.band_pass_filter_0_0, 0), (self.blocks_multiply_const_vxx_1_0, 0))
        self.connect((self.beamod_mvdr_beamformer_0, 0), (self.band_pass_filter_0_0, 0))
        self.connect((self.beamod_pilot_sync_0, 1), (self.beamod_mvdr_beamformer_0, 3))
        self.connect((self.beamod_pilot_sync_0, 0), (self.beamod_mvdr_beamformer_0, 2))
        self.connect((self.blocks_add_xx_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.beamod_mvdr_beamformer_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.blocks_add_xx_0_0, 0), (self.beamod_mvdr_beamformer_0, 1))
        self.connect((self.blocks_add_xx_0_1, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.blocks_add_xx_0_2, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_add_xx_0_3, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_add_xx_0_3_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_add_xx_0_3_1, 0), (self.blocks_multiply_const_vxx_0_0_0, 0))
        self.connect((self.blocks_add_xx_0_3_2, 0), (self.blocks_multiply_const_vxx_0_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_add_xx_0_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0_0_0, 0), (self.blocks_add_xx_0_1, 1))
        self.connect((self.blocks_multiply_const_vxx_0_0_0_0, 0), (self.blocks_add_xx_0_2, 1))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0, 0), (self.qtgui_freq_sink_x_0, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.beamod_pilot_sync_0, 1))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.beamod_pilot_sync_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.freq_xlating_fir_filter_xxx_0_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_add_xx_0_3, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.beamod_pilot_sync_0, 2))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.beamod_pilot_sync_0, 3))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "first_try_pa")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_freq_wave(self):
        return self.freq_wave

    def set_freq_wave(self, freq_wave):
        self.freq_wave = freq_wave
        self.set_wavelength(99792458.0 / self.freq_wave)
        self.analog_sig_source_x_0.set_frequency(self.freq_wave)
        self.analog_sig_source_x_0_0.set_frequency(self.freq_wave)
        self.analog_sig_source_x_0_1.set_frequency(self.freq_wave)
        self.analog_sig_source_x_0_2.set_frequency(self.freq_wave)
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.samp_rate, (0.9 * self.freq_wave), (1.1 * self.freq_wave), (0.01 * self.freq_wave), window.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(1, self.samp_rate, (0.9 * self.freq_wave), (1.1 * self.freq_wave), (0.01 * self.freq_wave), window.WIN_HAMMING, 6.76))

    def get_wavelength(self):
        return self.wavelength

    def set_wavelength(self, wavelength):
        self.wavelength = wavelength
        self.set_d_x(self.wavelength / 2)
        self.set_phase_shift(2 * np.pi * (self.d_x / self.wavelength) * np.sin(self.jammer_angle))

    def get_jammer_angle_deg(self):
        return self.jammer_angle_deg

    def set_jammer_angle_deg(self, jammer_angle_deg):
        self.jammer_angle_deg = jammer_angle_deg
        self.set_jammer_angle(np.radians(self.jammer_angle_deg))

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
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.samp_rate, (0.9 * self.freq_wave), (1.1 * self.freq_wave), (0.01 * self.freq_wave), window.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(1, self.samp_rate, (0.9 * self.freq_wave), (1.1 * self.freq_wave), (0.01 * self.freq_wave), window.WIN_HAMMING, 6.76))
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.low_pass(1.0, self.samp_rate, 10e3, 2e3))
        self.freq_xlating_fir_filter_xxx_0_0.set_taps(firdes.low_pass(1.0, self.samp_rate, 10e3, 2e3))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_pilot_offset(self):
        return self.pilot_offset

    def set_pilot_offset(self, pilot_offset):
        self.pilot_offset = pilot_offset
        self.analog_sig_source_x_0_3.set_frequency(self.pilot_offset)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq((-self.pilot_offset))
        self.freq_xlating_fir_filter_xxx_0_0.set_center_freq((-self.pilot_offset))

    def get_phase_shift(self):
        return self.phase_shift

    def set_phase_shift(self, phase_shift):
        self.phase_shift = phase_shift
        self.blocks_multiply_const_vxx_0.set_k(np.exp(-1j * 0 * self.phase_shift))
        self.blocks_multiply_const_vxx_0_0.set_k(np.exp(-1j * 1 * self.phase_shift))
        self.blocks_multiply_const_vxx_0_0_0.set_k(np.exp(-1j * 2 * self.phase_shift))
        self.blocks_multiply_const_vxx_0_0_0_0.set_k(np.exp(-1j * 3 * self.phase_shift))

    def get_c_light_speed(self):
        return self.c_light_speed

    def set_c_light_speed(self, c_light_speed):
        self.c_light_speed = c_light_speed

    def get_P_noise(self):
        return self.P_noise

    def set_P_noise(self, P_noise):
        self.P_noise = P_noise
        self.analog_noise_source_x_0.set_amplitude(self.P_noise)
        self.analog_noise_source_x_0_0.set_amplitude(self.P_noise)
        self.analog_noise_source_x_0_1.set_amplitude(self.P_noise)
        self.analog_noise_source_x_0_2.set_amplitude(self.P_noise)




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
