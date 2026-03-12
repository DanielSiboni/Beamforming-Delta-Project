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
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import numpy as np
import sip



class lms3(gr.top_block, Qt.QWidget):

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

        self.settings = Qt.QSettings("GNU Radio", "lms3")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.freq_wave = freq_wave = 2.4e3
        self.c_light_speed = c_light_speed = 299792458
        self.trans_degs = trans_degs = 10
        self.lambda_wave = lambda_wave = c_light_speed/freq_wave
        self.trans_theta_radians = trans_theta_radians = np.radians(trans_degs)
        self.d_x = d_x = lambda_wave / 2
        self.time_delay = time_delay = d_x*np.sin(trans_theta_radians)/c_light_speed
        self.samp_rate = samp_rate = 1e6
        self.recv_angle = recv_angle = 10
        self.noise_amp = noise_amp = 0.5

        ##################################################
        # Blocks
        ##################################################

        self._trans_degs_range = qtgui.Range(-90, 90, 0.01, 10, 200)
        self._trans_degs_win = qtgui.RangeWidget(self._trans_degs_range, self.set_trans_degs, "T Angle", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._trans_degs_win)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        self.qtgui_time_sink_x_1.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_1.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_1.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_win)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "Freqs", #name
            2,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0.set_fft_window_normalized(False)



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
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_0_win)
        self.blocks_streams_to_vector_0 = blocks.streams_to_vector(gr.sizeof_gr_complex*1, 3)
        self.blocks_delay_0_1_1 = blocks.delay(gr.sizeof_gr_complex*1, (2*int(time_delay*samp_rate)))
        self.blocks_delay_0_1_0 = blocks.delay(gr.sizeof_gr_complex*1, (2*int(time_delay*samp_rate)))
        self.blocks_delay_0_1 = blocks.delay(gr.sizeof_gr_complex*1, 0)
        self.blocks_delay_0_0_0 = blocks.delay(gr.sizeof_gr_complex*1, (1*int(time_delay*samp_rate)))
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_gr_complex*1, (1*int(time_delay*samp_rate)))
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, 0)
        self.blocks_add_xx_0_0_0_0 = blocks.add_vcc(1)
        self.blocks_add_xx_0_0_0 = blocks.add_vcc(1)
        self.blocks_add_xx_0_0 = blocks.add_vcc(1)
        self.beamod_lms_beamformer_0 = beamod.lms_beamformer(3, 0.001)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 2.4e3, 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 30e3, 0.1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.beamod_lms_beamformer_0, 1))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_delay_0_1_1, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_delay_0_0_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_delay_0_1, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_delay_0_1_0, 0))
        self.connect((self.beamod_lms_beamformer_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.beamod_lms_beamformer_0, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.blocks_add_xx_0_0, 0), (self.blocks_streams_to_vector_0, 0))
        self.connect((self.blocks_add_xx_0_0, 0), (self.qtgui_freq_sink_x_0_0, 1))
        self.connect((self.blocks_add_xx_0_0_0, 0), (self.blocks_streams_to_vector_0, 1))
        self.connect((self.blocks_add_xx_0_0_0_0, 0), (self.blocks_streams_to_vector_0, 2))
        self.connect((self.blocks_delay_0, 0), (self.blocks_add_xx_0_0, 1))
        self.connect((self.blocks_delay_0_0, 0), (self.blocks_add_xx_0_0_0, 0))
        self.connect((self.blocks_delay_0_0_0, 0), (self.blocks_add_xx_0_0_0, 1))
        self.connect((self.blocks_delay_0_1, 0), (self.blocks_add_xx_0_0, 0))
        self.connect((self.blocks_delay_0_1_0, 0), (self.blocks_add_xx_0_0_0_0, 1))
        self.connect((self.blocks_delay_0_1_1, 0), (self.blocks_add_xx_0_0_0_0, 0))
        self.connect((self.blocks_streams_to_vector_0, 0), (self.beamod_lms_beamformer_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "lms3")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_freq_wave(self):
        return self.freq_wave

    def set_freq_wave(self, freq_wave):
        self.freq_wave = freq_wave
        self.set_lambda_wave(self.c_light_speed/self.freq_wave)

    def get_c_light_speed(self):
        return self.c_light_speed

    def set_c_light_speed(self, c_light_speed):
        self.c_light_speed = c_light_speed
        self.set_lambda_wave(self.c_light_speed/self.freq_wave)
        self.set_time_delay(self.d_x*np.sin(self.trans_theta_radians)/self.c_light_speed)

    def get_trans_degs(self):
        return self.trans_degs

    def set_trans_degs(self, trans_degs):
        self.trans_degs = trans_degs
        self.set_trans_theta_radians(np.radians(self.trans_degs))

    def get_lambda_wave(self):
        return self.lambda_wave

    def set_lambda_wave(self, lambda_wave):
        self.lambda_wave = lambda_wave
        self.set_d_x(self.lambda_wave / 2)

    def get_trans_theta_radians(self):
        return self.trans_theta_radians

    def set_trans_theta_radians(self, trans_theta_radians):
        self.trans_theta_radians = trans_theta_radians
        self.set_time_delay(self.d_x*np.sin(self.trans_theta_radians)/self.c_light_speed)

    def get_d_x(self):
        return self.d_x

    def set_d_x(self, d_x):
        self.d_x = d_x
        self.set_time_delay(self.d_x*np.sin(self.trans_theta_radians)/self.c_light_speed)

    def get_time_delay(self):
        return self.time_delay

    def set_time_delay(self, time_delay):
        self.time_delay = time_delay
        self.blocks_delay_0_0.set_dly(int((1*int(self.time_delay*self.samp_rate))))
        self.blocks_delay_0_0_0.set_dly(int((1*int(self.time_delay*self.samp_rate))))
        self.blocks_delay_0_1_0.set_dly(int((2*int(self.time_delay*self.samp_rate))))
        self.blocks_delay_0_1_1.set_dly(int((2*int(self.time_delay*self.samp_rate))))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.blocks_delay_0_0.set_dly(int((1*int(self.time_delay*self.samp_rate))))
        self.blocks_delay_0_0_0.set_dly(int((1*int(self.time_delay*self.samp_rate))))
        self.blocks_delay_0_1_0.set_dly(int((2*int(self.time_delay*self.samp_rate))))
        self.blocks_delay_0_1_1.set_dly(int((2*int(self.time_delay*self.samp_rate))))
        self.qtgui_freq_sink_x_0_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate)

    def get_recv_angle(self):
        return self.recv_angle

    def set_recv_angle(self, recv_angle):
        self.recv_angle = recv_angle

    def get_noise_amp(self):
        return self.noise_amp

    def set_noise_amp(self, noise_amp):
        self.noise_amp = noise_amp




def main(top_block_cls=lms3, options=None):

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
