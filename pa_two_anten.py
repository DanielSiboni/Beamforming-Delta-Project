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
from gnuradio import uhd
import time
import numpy as np
import sip



class pa_two_anten(gr.top_block, Qt.QWidget):

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

        self.settings = Qt.QSettings("GNU Radio", "pa_two_anten")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.freq_wave = freq_wave = 2.4e9
        self.c_light_speed = c_light_speed = 299792458
        self.lambda_wave = lambda_wave = c_light_speed/freq_wave
        self.recv_theta = recv_theta = 0
        self.d_x = d_x = lambda_wave / 2
        self.samp_rate = samp_rate = 5e6
        self.r_gain = r_gain = 20
        self.phase_diff = phase_diff = 2*np.pi* d_x * np.sin(recv_theta) / lambda_wave

        ##################################################
        # Blocks
        ##################################################

        self._r_gain_range = qtgui.Range(0, 50, 1, 20, 200)
        self._r_gain_win = qtgui.RangeWidget(self._r_gain_range, self.set_r_gain, "Reciver Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._r_gain_win)
        self.uhd_usrp_source_0_0 = uhd.usrp_source(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,2)),
            ),
        )
        self.uhd_usrp_source_0_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_source_0_0.set_center_freq(freq_wave, 0)
        self.uhd_usrp_source_0_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_source_0_0.set_gain(r_gain, 0)

        self.uhd_usrp_source_0_0.set_center_freq(freq_wave, 1)
        self.uhd_usrp_source_0_0.set_antenna("TX/RX", 1)
        self.uhd_usrp_source_0_0.set_gain(r_gain, 1)
        self._recv_theta_range = qtgui.Range(-np.pi / 2, np.pi / 2, 0.01, 0, 200)
        self._recv_theta_win = qtgui.RangeWidget(self._recv_theta_range, self.set_recv_theta, "R Angle", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._recv_theta_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            freq_wave, #fc
            samp_rate, #bw
            "Freqs", #name
            1,
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

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.blocks_phase_shift_0_0 = blocks.phase_shift(1*phase_diff, True)
        self.blocks_phase_shift_0 = blocks.phase_shift(0*phase_diff, True)
        self.blocks_add_xx_0 = blocks.add_vcc(1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_xx_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_phase_shift_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_phase_shift_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.uhd_usrp_source_0_0, 0), (self.blocks_phase_shift_0, 0))
        self.connect((self.uhd_usrp_source_0_0, 1), (self.blocks_phase_shift_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "pa_two_anten")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_freq_wave(self):
        return self.freq_wave

    def set_freq_wave(self, freq_wave):
        self.freq_wave = freq_wave
        self.set_lambda_wave(self.c_light_speed/self.freq_wave)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.freq_wave, self.samp_rate)
        self.uhd_usrp_source_0_0.set_center_freq(self.freq_wave, 0)
        self.uhd_usrp_source_0_0.set_center_freq(self.freq_wave, 1)

    def get_c_light_speed(self):
        return self.c_light_speed

    def set_c_light_speed(self, c_light_speed):
        self.c_light_speed = c_light_speed
        self.set_lambda_wave(self.c_light_speed/self.freq_wave)

    def get_lambda_wave(self):
        return self.lambda_wave

    def set_lambda_wave(self, lambda_wave):
        self.lambda_wave = lambda_wave
        self.set_d_x(self.lambda_wave / 2)
        self.set_phase_diff(2*np.pi* self.d_x * np.sin(self.recv_theta) / self.lambda_wave )

    def get_recv_theta(self):
        return self.recv_theta

    def set_recv_theta(self, recv_theta):
        self.recv_theta = recv_theta
        self.set_phase_diff(2*np.pi* self.d_x * np.sin(self.recv_theta) / self.lambda_wave )

    def get_d_x(self):
        return self.d_x

    def set_d_x(self, d_x):
        self.d_x = d_x
        self.set_phase_diff(2*np.pi* self.d_x * np.sin(self.recv_theta) / self.lambda_wave )

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_freq_sink_x_0.set_frequency_range(self.freq_wave, self.samp_rate)
        self.uhd_usrp_source_0_0.set_samp_rate(self.samp_rate)

    def get_r_gain(self):
        return self.r_gain

    def set_r_gain(self, r_gain):
        self.r_gain = r_gain
        self.uhd_usrp_source_0_0.set_gain(self.r_gain, 0)
        self.uhd_usrp_source_0_0.set_gain(self.r_gain, 1)

    def get_phase_diff(self):
        return self.phase_diff

    def set_phase_diff(self, phase_diff):
        self.phase_diff = phase_diff
        self.blocks_phase_shift_0.set_shift(0*self.phase_diff)
        self.blocks_phase_shift_0_0.set_shift(1*self.phase_diff)




def main(top_block_cls=pa_two_anten, options=None):

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
