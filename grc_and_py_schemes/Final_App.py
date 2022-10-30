#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Aplicacion_Final
# GNU Radio version: 3.9.0.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
import numpy
from gnuradio import channels
from gnuradio import digital
from gnuradio import fec
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio.filter import pfb
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import TFMv5



from gnuradio import qtgui

class Aplicacion_Final(gr.top_block, Qt.QWidget):

    def __init__(self, hdr_const=digital.psk_constellation(2,digital.mod_codes.GRAY_CODE), hdr_format=digital.header_format_default(digital.packet_utils.default_access_code, 0,1), hdr_format_16qam=TFMv5.header_format_counter_dif(digital.packet_utils.default_access_code, 0,4), hdr_format_64qam=TFMv5.header_format_counter_dif(digital.packet_utils.default_access_code, 0,6), hdr_format_bpsk=TFMv5.header_format_counter_dif(digital.packet_utils.default_access_code, 0,1), hdr_format_bpsk_copy=TFMv5.header_format_counter_dif(digital.packet_utils.default_access_code, 0,1), hdr_format_qpsk=TFMv5.header_format_counter_dif(digital.packet_utils.default_access_code, 0,2)):
        gr.top_block.__init__(self, "Aplicacion_Final", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Aplicacion_Final")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
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

        self.settings = Qt.QSettings("GNU Radio", "Aplicacion_Final")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Parameters
        ##################################################
        self.hdr_const = hdr_const
        self.hdr_format = hdr_format
        self.hdr_format_16qam = hdr_format_16qam
        self.hdr_format_64qam = hdr_format_64qam
        self.hdr_format_bpsk = hdr_format_bpsk
        self.hdr_format_bpsk_copy = hdr_format_bpsk_copy
        self.hdr_format_qpsk = hdr_format_qpsk

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 4
        self.nfilts = nfilts = 32
        self.eb = eb = 0.35
        self.psf_taps = psf_taps = firdes.root_raised_cosine(nfilts, nfilts,1.0, eb, 15*sps*nfilts)
        self.taps_per_filt = taps_per_filt = int(len(psf_taps)/nfilts)
        self.rxmod = rxmod = digital.generic_mod(hdr_const, True, sps, True, eb, False, False)
        self.preamble = preamble = [0xac, 0xdd, 0xa4, 0xe2, 0xf2, 0x8c, 0x20, 0xfc]
        self.d = d = 1/(2**(1/2))
        self.timing_loop_bw = timing_loop_bw = 6.28/200
        self.taps = taps = [0.9,0,0,0,0.3,0,0,0,0.312]
        self.scale_64QAM = scale_64QAM = 0.9393
        self.scale_16QAM = scale_16QAM = 0.9471
        self.samp_rate = samp_rate = 1e6
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps), eb, 11*sps*nfilts)
        self.pld_const_qpsk = pld_const_qpsk = digital.constellation_rect([d+d*1j, -d+d*1j,-d-d*1j, d-d*1j], [0, 1, 3, 2],
        4, 2, 2, 1, 1).base()
        self.pld_const_64qam = pld_const_64qam = digital.qam_constellation(64,True,digital.mod_codes.GRAY_CODE,False)
        self.pld_const_16qam = pld_const_16qam = digital.qam_constellation(16,True,digital.mod_codes.GRAY_CODE,False)
        self.noise_volt = noise_volt = 0
        self.modulated_sync_word = modulated_sync_word = digital.modulate_vector_bc(rxmod.to_basic_block(), preamble, [1])
        self.mark_delay = mark_delay = 104
        self.gain_tx = gain_tx = 40
        self.gain_rx = gain_rx = 30
        self.freq_offset = freq_offset = 0
        self.freq2 = freq2 = 750e6
        self.freq = freq = 800e6
        self.filt_delay = filt_delay = int(1+(taps_per_filt-1)//2)
        self.dec_dummy_0 = dec_dummy_0 = fec.dummy_decoder.make(12*8)
        self.dec_dummy = dec_dummy = fec.dummy_decoder.make(18*8)

        ##################################################
        # Blocks
        ##################################################
        self.controls = Qt.QTabWidget()
        self.controls_widget_0 = Qt.QWidget()
        self.controls_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.controls_widget_0)
        self.controls_grid_layout_0 = Qt.QGridLayout()
        self.controls_layout_0.addLayout(self.controls_grid_layout_0)
        self.controls.addTab(self.controls_widget_0, 'Channel')
        self.controls_widget_1 = Qt.QWidget()
        self.controls_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.controls_widget_1)
        self.controls_grid_layout_1 = Qt.QGridLayout()
        self.controls_layout_1.addLayout(self.controls_grid_layout_1)
        self.controls.addTab(self.controls_widget_1, 'Tx')
        self.top_grid_layout.addWidget(self.controls, 0, 0, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._noise_volt_range = Range(0, 2, 0.0001, 0, 200)
        self._noise_volt_win = RangeWidget(self._noise_volt_range, self.set_noise_volt, 'Noise Voltage', "counter_slider", float, QtCore.Qt.Horizontal)
        self.controls_grid_layout_0.addWidget(self._noise_volt_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.controls_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.controls_grid_layout_0.setColumnStretch(c, 1)
        self._gain_tx_range = Range(30, 40, 1, 40, 200)
        self._gain_tx_win = RangeWidget(self._gain_tx_range, self.set_gain_tx, 'gain_tx', "counter_slider", float, QtCore.Qt.Horizontal)
        self.controls_grid_layout_1.addWidget(self._gain_tx_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.controls_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.controls_grid_layout_1.setColumnStretch(c, 1)
        self._freq_offset_range = Range(-0.1, 0.1, 0.001, 0, 200)
        self._freq_offset_win = RangeWidget(self._freq_offset_range, self.set_freq_offset, 'Frequency Offset', "counter_slider", float, QtCore.Qt.Horizontal)
        self.controls_grid_layout_0.addWidget(self._freq_offset_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.controls_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.controls_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_2 = qtgui.time_sink_c(
            1024*10, #size
            1e6, #samp_rate
            "Rx_Tx Signal", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_2.set_update_time(0.10)
        self.qtgui_time_sink_x_0_2.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0_2.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_2.enable_tags(True)
        self.qtgui_time_sink_x_0_2.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_2.enable_autoscale(False)
        self.qtgui_time_sink_x_0_2.enable_grid(True)
        self.qtgui_time_sink_x_0_2.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_2.enable_control_panel(False)
        self.qtgui_time_sink_x_0_2.enable_stem_plot(False)


        labels = ['I', 'Q', 'Signal 3', 'Signal 4', 'Signal 5',
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
                    self.qtgui_time_sink_x_0_2.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_2.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_2.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_2.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_2.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_2.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_2.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_2.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_2_win = sip.wrapinstance(self.qtgui_time_sink_x_0_2.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_2_win, 5, 1, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_c(
            1024*4, #size
            1e6, #samp_rate
            "Ph Clock Out", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(True)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


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
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024*10, #size
            1e6, #samp_rate
            "Tx Signal", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, '')
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


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
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0_1 = qtgui.const_sink_c(
            128, #size
            "Tx_Rx Header", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_1.set_update_time(0.10)
        self.qtgui_const_sink_x_0_1.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0_1.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_1.enable_autoscale(False)
        self.qtgui_const_sink_x_0_1.enable_grid(True)
        self.qtgui_const_sink_x_0_1.enable_axis_labels(True)


        labels = ['Const', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_1.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_1.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_1.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_1.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_1_win = sip.wrapinstance(self.qtgui_const_sink_x_0_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_1_win, 5, 0, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0_0_1_0 = qtgui.const_sink_c(
            1024, #size
            "64QAM", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_0_1_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0_0_1_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0_0_1_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0_0_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_0_1_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0_0_1_0.enable_grid(True)
        self.qtgui_const_sink_x_0_0_1_0.enable_axis_labels(True)


        labels = ['Const', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_0_1_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_0_1_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_0_1_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_0_1_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_0_1_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_0_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_0_1_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_0_1_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_0_1_0_win, 4, 0, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0_0_1 = qtgui.const_sink_c(
            1024, #size
            "16QAM", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_0_1.set_update_time(0.10)
        self.qtgui_const_sink_x_0_0_1.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0_0_1.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_0_1.enable_autoscale(False)
        self.qtgui_const_sink_x_0_0_1.enable_grid(True)
        self.qtgui_const_sink_x_0_0_1.enable_axis_labels(True)


        labels = ['Const', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_0_1.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_0_1.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_0_1.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_0_1.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_0_1.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_0_1_win = sip.wrapinstance(self.qtgui_const_sink_x_0_0_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_0_1_win, 3, 1, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0_0_0_0 = qtgui.const_sink_c(
            128, #size
            "Tx_Rx Payload", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_0_0_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0_0_0_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0_0_0_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_0_0_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0_0_0_0.enable_grid(True)
        self.qtgui_const_sink_x_0_0_0_0.enable_axis_labels(True)


        labels = ['Const', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_0_0_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_0_0_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_0_0_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_0_0_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_0_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_0_0_0_win, 4, 1, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0_0_0 = qtgui.const_sink_c(
            128, #size
            "BPSK", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_0_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0_0_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0_0_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_0_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0_0_0.enable_grid(True)
        self.qtgui_const_sink_x_0_0_0.enable_axis_labels(True)


        labels = ['Const', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_0_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_0_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_0_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_0_0_win, 2, 1, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0_0 = qtgui.const_sink_c(
            512, #size
            "QPSK", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0_0.enable_grid(True)
        self.qtgui_const_sink_x_0_0.enable_axis_labels(True)


        labels = ['Const', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_0_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            128, #size
            "Header Constellation", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(True)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['Const', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.uhd_usrp_source_0_0 = uhd.usrp_source(
            ",".join(("serial=30F9A69", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0_0.set_samp_rate(samp_rate/4)
        # No synchronization enforced.

        self.uhd_usrp_source_0_0.set_center_freq(freq2, 0)
        self.uhd_usrp_source_0_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0_0.set_gain(gain_rx, 0)
        self.uhd_usrp_source_0_0.set_auto_dc_offset(False, 0)
        self.uhd_usrp_source_0_0.set_auto_iq_balance(False, 0)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("serial=30F9A6B", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        # No synchronization enforced.

        self.uhd_usrp_source_0.set_center_freq(freq, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_rx_agc(False, 0)
        self.uhd_usrp_source_0.set_gain(gain_rx, 0)
        self.uhd_usrp_source_0.set_auto_dc_offset(False, 0)
        self.uhd_usrp_source_0.set_auto_iq_balance(False, 0)
        self.uhd_usrp_sink_0_0 = uhd.usrp_sink(
            ",".join(("serial=30F9A6B", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            '',
        )
        self.uhd_usrp_sink_0_0.set_samp_rate(samp_rate/4)
        self.uhd_usrp_sink_0_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_sink_0_0.set_center_freq(freq2, 0)
        self.uhd_usrp_sink_0_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0_0.set_gain(gain_rx, 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("serial=30F9A69", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            '',
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_sink_0.set_center_freq(freq, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_gain(gain_tx, 0)
        self.pfb_arb_resampler_xxx_0_0_1 = pfb.arb_resampler_ccf(
            sps,
            taps=psf_taps,
            flt_size=nfilts)
        self.pfb_arb_resampler_xxx_0_0_1.declare_sample_delay(filt_delay)
        self.pfb_arb_resampler_xxx_0_0_0_1 = pfb.arb_resampler_ccf(
            sps,
            taps=psf_taps,
            flt_size=nfilts)
        self.pfb_arb_resampler_xxx_0_0_0_1.declare_sample_delay(filt_delay)
        self.pfb_arb_resampler_xxx_0_0_0_0_0_0_0 = pfb.arb_resampler_ccf(
            sps,
            taps=psf_taps,
            flt_size=nfilts)
        self.pfb_arb_resampler_xxx_0_0_0_0_0_0_0.declare_sample_delay(filt_delay)
        self.pfb_arb_resampler_xxx_0_0_0_0_0_0 = pfb.arb_resampler_ccf(
            sps,
            taps=psf_taps,
            flt_size=nfilts)
        self.pfb_arb_resampler_xxx_0_0_0_0_0_0.declare_sample_delay(filt_delay)
        self.pfb_arb_resampler_xxx_0_0_0_0_0 = pfb.arb_resampler_ccf(
            sps,
            taps=psf_taps,
            flt_size=nfilts)
        self.pfb_arb_resampler_xxx_0_0_0_0_0.declare_sample_delay(filt_delay)
        self.pfb_arb_resampler_xxx_0_0_0_0 = pfb.arb_resampler_ccf(
            sps,
            taps=psf_taps,
            flt_size=nfilts)
        self.pfb_arb_resampler_xxx_0_0_0_0.declare_sample_delay(filt_delay)
        self.pfb_arb_resampler_xxx_0_0_0 = pfb.arb_resampler_ccf(
            sps,
            taps=psf_taps,
            flt_size=nfilts)
        self.pfb_arb_resampler_xxx_0_0_0.declare_sample_delay(filt_delay)
        self.pfb_arb_resampler_xxx_0_0 = pfb.arb_resampler_ccf(
            sps,
            taps=psf_taps,
            flt_size=nfilts)
        self.pfb_arb_resampler_xxx_0_0.declare_sample_delay(filt_delay)
        self.fec_generic_decoder_0_0_0 = fec.decoder(dec_dummy_0, gr.sizeof_float, gr.sizeof_char)
        self.fec_generic_decoder_0_0 = fec.decoder(dec_dummy, gr.sizeof_float, gr.sizeof_char)
        self.digital_protocol_parser_b_0_0 = digital.protocol_parser_b(hdr_format)
        self.digital_protocol_parser_b_0 = digital.protocol_parser_b(hdr_format_bpsk_copy)
        self.digital_protocol_formatter_bb_0_1_0_0_0 = digital.protocol_formatter_bb(hdr_format, "packet_len")
        self.digital_protocol_formatter_bb_0_1_0_0 = digital.protocol_formatter_bb(hdr_format, "packet_len")
        self.digital_protocol_formatter_bb_0_1_0 = digital.protocol_formatter_bb(hdr_format, "packet_len")
        self.digital_protocol_formatter_bb_0_1 = digital.protocol_formatter_bb(hdr_format, "packet_len")
        self.digital_protocol_formatter_bb_0_0_0_0 = digital.protocol_formatter_bb(hdr_format_64qam, "packet_len")
        self.digital_protocol_formatter_bb_0_0_0 = digital.protocol_formatter_bb(hdr_format_16qam, "packet_len")
        self.digital_protocol_formatter_bb_0_0 = digital.protocol_formatter_bb(hdr_format_bpsk, "packet_len")
        self.digital_protocol_formatter_bb_0 = digital.protocol_formatter_bb(hdr_format_qpsk, "packet_len")
        self.digital_pfb_clock_sync_xxx_0_0 = digital.pfb_clock_sync_ccf(sps, timing_loop_bw*2, rrc_taps, nfilts, nfilts/2, 1.5, 2)
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(sps, timing_loop_bw*2, rrc_taps, nfilts, nfilts/2, 1.5, 2)
        self.digital_lms_dd_equalizer_cc_2_0_0_0 = digital.lms_dd_equalizer_cc(15, 1e-9, 1, pld_const_16qam)
        self.digital_lms_dd_equalizer_cc_0 = digital.lms_dd_equalizer_cc(15, 1e-9, 1, pld_const_64qam)
        self.digital_header_payload_demux_0 = digital.header_payload_demux(
            (hdr_format.header_nbits()) //  hdr_const.bits_per_symbol(),
            1,
            0,
            "payload symbols",
            "amp_est",
            True,
            gr.sizeof_gr_complex,
            "rx_time",
            1,
            [],
            0)
        self.digital_fll_band_edge_cc_0_0 = digital.fll_band_edge_cc(sps, eb, 256, 2e-3)
        self.digital_fll_band_edge_cc_0 = digital.fll_band_edge_cc(sps, eb, 256, 2e-3)
        self.digital_diff_encoder_bb_0_3_0_0_0 = digital.diff_encoder_bb(len(hdr_const.points()))
        self.digital_diff_encoder_bb_0_3_0_0 = digital.diff_encoder_bb(len(hdr_const.points()))
        self.digital_diff_encoder_bb_0_3_0 = digital.diff_encoder_bb(len(hdr_const.points()))
        self.digital_diff_encoder_bb_0_3 = digital.diff_encoder_bb(len(hdr_const.points()))
        self.digital_diff_encoder_bb_0_2_0 = digital.diff_encoder_bb(len(hdr_const.points()))
        self.digital_diff_encoder_bb_0_2 = digital.diff_encoder_bb(len(hdr_const.points()))
        self.digital_diff_encoder_bb_0_1 = digital.diff_encoder_bb(len(hdr_const.points()))
        self.digital_diff_encoder_bb_0_0_2_0_0_0 = digital.diff_encoder_bb(len(hdr_const.points()))
        self.digital_diff_encoder_bb_0_0_2_0_0 = digital.diff_encoder_bb(len(hdr_const.points()))
        self.digital_diff_encoder_bb_0_0_2_0 = digital.diff_encoder_bb(len(hdr_const.points()))
        self.digital_diff_encoder_bb_0_0_2 = digital.diff_encoder_bb(len(hdr_const.points()))
        self.digital_diff_encoder_bb_0_0_1_0 = digital.diff_encoder_bb(len(pld_const_64qam.points()))
        self.digital_diff_encoder_bb_0_0_1 = digital.diff_encoder_bb(len(pld_const_16qam.points()))
        self.digital_diff_encoder_bb_0_0_0 = digital.diff_encoder_bb(len(hdr_const.points()))
        self.digital_diff_encoder_bb_0_0 = digital.diff_encoder_bb(len(pld_const_qpsk.points()))
        self.digital_diff_encoder_bb_0 = digital.diff_encoder_bb(len(hdr_const.points()))
        self.digital_diff_decoder_bb_0_0_0_2_0 = digital.diff_decoder_bb(len(pld_const_64qam.points()))
        self.digital_diff_decoder_bb_0_0_0_2 = digital.diff_decoder_bb(len(pld_const_16qam.points()))
        self.digital_diff_decoder_bb_0_0_0_1_0 = digital.diff_decoder_bb(len(hdr_const.points()))
        self.digital_diff_decoder_bb_0_0_0_1 = digital.diff_decoder_bb(len(hdr_const.points()))
        self.digital_diff_decoder_bb_0_0_0_0_0 = digital.diff_decoder_bb(len(hdr_const.points()))
        self.digital_diff_decoder_bb_0_0_0_0 = digital.diff_decoder_bb(len(hdr_const.points()))
        self.digital_diff_decoder_bb_0_0_0 = digital.diff_decoder_bb(len(pld_const_qpsk.points()))
        self.digital_crc32_bb_0_1_0_0_0 = digital.crc32_bb(False, "packet_len", True)
        self.digital_crc32_bb_0_1_0_0 = digital.crc32_bb(False, "packet_len", True)
        self.digital_crc32_bb_0_1_0 = digital.crc32_bb(False, "packet_len", True)
        self.digital_crc32_bb_0_1 = digital.crc32_bb(False, "packet_len", True)
        self.digital_crc32_bb_0_0_0_0 = digital.crc32_bb(False, "packet_len", True)
        self.digital_crc32_bb_0_0_0 = digital.crc32_bb(False, "packet_len", True)
        self.digital_crc32_bb_0_0 = digital.crc32_bb(False, "packet_len", True)
        self.digital_crc32_bb_0 = digital.crc32_bb(False, "packet_len", True)
        self.digital_crc32_async_bb_0_0_0 = digital.crc32_async_bb(True)
        self.digital_costas_loop_cc_0_0_1 = digital.costas_loop_cc(6.28/100, hdr_const.arity(), False)
        self.digital_costas_loop_cc_0_0_0_0_0 = digital.costas_loop_cc(6.28/100, hdr_const.arity(), False)
        self.digital_costas_loop_cc_0_0_0_0 = digital.costas_loop_cc(6.28/100, hdr_const.arity(), False)
        self.digital_costas_loop_cc_0_0_0 = digital.costas_loop_cc(6.28/100, pld_const_qpsk.arity(), False)
        self.digital_costas_loop_cc_0_0 = digital.costas_loop_cc(6.28/100, hdr_const.arity(), False)
        self.digital_corr_est_cc_0_0 = digital.corr_est_cc(modulated_sync_word, sps, mark_delay, 0.7, digital.THRESHOLD_ABSOLUTE)
        self.digital_corr_est_cc_0 = digital.corr_est_cc(modulated_sync_word, sps, mark_delay, 0.5, digital.THRESHOLD_ABSOLUTE)
        self.digital_constellation_soft_decoder_cf_0_0_0 = digital.constellation_soft_decoder_cf(hdr_const)
        self.digital_constellation_soft_decoder_cf_0_0 = digital.constellation_soft_decoder_cf(hdr_const)
        self.digital_constellation_receiver_cb_0_0 = digital.constellation_receiver_cb(pld_const_64qam.base(), 6.28/100, -0.5, 0.5)
        self.digital_constellation_receiver_cb_0 = digital.constellation_receiver_cb(pld_const_16qam, 6.28/100, -0.5, 0.5)
        self.digital_constellation_decoder_cb_0_0_1 = digital.constellation_decoder_cb(pld_const_16qam)
        self.digital_constellation_decoder_cb_0_0_0_0 = digital.constellation_decoder_cb(hdr_const)
        self.digital_constellation_decoder_cb_0_0_0 = digital.constellation_decoder_cb(hdr_const)
        self.digital_constellation_decoder_cb_0_0 = digital.constellation_decoder_cb(pld_const_qpsk)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(pld_const_64qam.base())
        self.digital_cma_equalizer_cc_0_0_0_1_0 = digital.cma_equalizer_cc(15, 1.5655, 1e-6, 1)
        self.digital_cma_equalizer_cc_0_0_0_1 = digital.cma_equalizer_cc(15, 1, 1e-6, 2)
        self.digital_cma_equalizer_cc_0_0_0_0_0_0 = digital.cma_equalizer_cc(15, 1, 1e-6, 1)
        self.digital_cma_equalizer_cc_0_0_0_0_0 = digital.cma_equalizer_cc(15, 1, 1e-6, 1)
        self.digital_cma_equalizer_cc_0_0_0_0 = digital.cma_equalizer_cc(15, 1, 1e-6, 1)
        self.digital_cma_equalizer_cc_0_0_0 = digital.cma_equalizer_cc(15, 1, 1e-6, 2)
        self.digital_chunks_to_symbols_xx_0_3_0_0_0 = digital.chunks_to_symbols_bc(hdr_const.points(), 1)
        self.digital_chunks_to_symbols_xx_0_3_0_0 = digital.chunks_to_symbols_bc(hdr_const.points(), 1)
        self.digital_chunks_to_symbols_xx_0_3_0 = digital.chunks_to_symbols_bc(hdr_const.points(), 1)
        self.digital_chunks_to_symbols_xx_0_3 = digital.chunks_to_symbols_bc(hdr_const.points(), 1)
        self.digital_chunks_to_symbols_xx_0_2_0 = digital.chunks_to_symbols_bc(hdr_const.points(), 1)
        self.digital_chunks_to_symbols_xx_0_2 = digital.chunks_to_symbols_bc(hdr_const.points(), 1)
        self.digital_chunks_to_symbols_xx_0_1 = digital.chunks_to_symbols_bc(hdr_const.points(), 1)
        self.digital_chunks_to_symbols_xx_0_0_2_0_0_0 = digital.chunks_to_symbols_bc(hdr_const.points(), 1)
        self.digital_chunks_to_symbols_xx_0_0_2_0_0 = digital.chunks_to_symbols_bc(hdr_const.points(), 1)
        self.digital_chunks_to_symbols_xx_0_0_2_0 = digital.chunks_to_symbols_bc(hdr_const.points(), 1)
        self.digital_chunks_to_symbols_xx_0_0_2 = digital.chunks_to_symbols_bc(hdr_const.points(), 1)
        self.digital_chunks_to_symbols_xx_0_0_1_0 = digital.chunks_to_symbols_bc(pld_const_64qam.points(), 1)
        self.digital_chunks_to_symbols_xx_0_0_1 = digital.chunks_to_symbols_bc(pld_const_16qam.points(), 1)
        self.digital_chunks_to_symbols_xx_0_0_0 = digital.chunks_to_symbols_bc(hdr_const.points(), 1)
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bc(pld_const_qpsk.points(), 1)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc(hdr_const.points(), 1)
        self.channels_channel_model_0_0 = channels.channel_model(
            noise_voltage=noise_volt,
            frequency_offset=freq_offset,
            epsilon=1,
            taps=[1],
            noise_seed=0,
            block_tags=False)
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=noise_volt,
            frequency_offset=freq_offset,
            epsilon=1,
            taps=[1],
            noise_seed=0,
            block_tags=False)
        self.blocks_vector_source_x_0_0_0_0 = blocks.vector_source_b([255], True, 1, [])
        self.blocks_vector_source_x_0_0_0 = blocks.vector_source_b([170], True, 1, [])
        self.blocks_vector_source_x_0_0 = blocks.vector_source_b([85], True, 1, [])
        self.blocks_vector_source_x_0 = blocks.vector_source_b([0], True, 1, [])
        self.blocks_tagged_stream_to_pdu_0_1_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, "payload symbols")
        self.blocks_tagged_stream_to_pdu_0_1 = blocks.tagged_stream_to_pdu(blocks.byte_t, "payload symbols")
        self.blocks_tagged_stream_to_pdu_0_0_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, "payload symbols")
        self.blocks_tagged_stream_to_pdu_0_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, "payload symbols")
        self.blocks_tagged_stream_to_pdu_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, "payload symbols")
        self.blocks_tagged_stream_mux_0_2_2_0_0_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, 'packet_len', 0)
        self.blocks_tagged_stream_mux_0_2_2_0_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, 'packet_len', 0)
        self.blocks_tagged_stream_mux_0_2_2_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, 'packet_len', 0)
        self.blocks_tagged_stream_mux_0_2_2 = blocks.tagged_stream_mux(gr.sizeof_char*1, 'packet_len', 0)
        self.blocks_tagged_stream_mux_0_2_0_0_0 = blocks.tagged_stream_mux(gr.sizeof_gr_complex*1, 'packet_len', 0)
        self.blocks_tagged_stream_mux_0_2_0_0 = blocks.tagged_stream_mux(gr.sizeof_gr_complex*1, 'packet_len', 0)
        self.blocks_tagged_stream_mux_0_2_0 = blocks.tagged_stream_mux(gr.sizeof_gr_complex*1, 'packet_len', 0)
        self.blocks_tagged_stream_mux_0_2 = blocks.tagged_stream_mux(gr.sizeof_gr_complex*1, 'packet_len', 0)
        self.blocks_tagged_stream_mux_0_1_0 = blocks.tagged_stream_mux(gr.sizeof_gr_complex*1, 'packet_len', 0)
        self.blocks_tagged_stream_mux_0_1 = blocks.tagged_stream_mux(gr.sizeof_gr_complex*1, 'packet_len', 0)
        self.blocks_tagged_stream_mux_0_0 = blocks.tagged_stream_mux(gr.sizeof_gr_complex*1, 'packet_len', 0)
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_gr_complex*1, 'packet_len', 0)
        self.blocks_tagged_stream_multiply_length_0_0_1 = blocks.tagged_stream_multiply_length(gr.sizeof_gr_complex*1, 'packet_len', sps)
        self.blocks_tagged_stream_multiply_length_0_0_0_1 = blocks.tagged_stream_multiply_length(gr.sizeof_gr_complex*1, 'packet_len', sps)
        self.blocks_tagged_stream_multiply_length_0_0_0_0_0_0_0 = blocks.tagged_stream_multiply_length(gr.sizeof_gr_complex*1, 'packet_len', sps)
        self.blocks_tagged_stream_multiply_length_0_0_0_0_0_0 = blocks.tagged_stream_multiply_length(gr.sizeof_gr_complex*1, 'packet_len', sps)
        self.blocks_tagged_stream_multiply_length_0_0_0_0_0 = blocks.tagged_stream_multiply_length(gr.sizeof_gr_complex*1, 'packet_len', sps)
        self.blocks_tagged_stream_multiply_length_0_0_0_0 = blocks.tagged_stream_multiply_length(gr.sizeof_gr_complex*1, 'packet_len', sps)
        self.blocks_tagged_stream_multiply_length_0_0_0 = blocks.tagged_stream_multiply_length(gr.sizeof_gr_complex*1, 'packet_len', sps)
        self.blocks_tagged_stream_multiply_length_0_0 = blocks.tagged_stream_multiply_length(gr.sizeof_gr_complex*1, 'packet_len', sps)
        self.blocks_tag_gate_0_0_0 = blocks.tag_gate(gr.sizeof_gr_complex * 1, False)
        self.blocks_tag_gate_0_0_0.set_single_key("time_est")
        self.blocks_tag_gate_0_0 = blocks.tag_gate(gr.sizeof_gr_complex * 1, False)
        self.blocks_tag_gate_0_0.set_single_key("time_est")
        self.blocks_stream_to_tagged_stream_0_1_2_0_0_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 12, "packet_len")
        self.blocks_stream_to_tagged_stream_0_1_2_0_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 12, "packet_len")
        self.blocks_stream_to_tagged_stream_0_1_2_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 12, "packet_len")
        self.blocks_stream_to_tagged_stream_0_1_2 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 12, "packet_len")
        self.blocks_stream_to_tagged_stream_0_1_0_0_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 2, "packet_len")
        self.blocks_stream_to_tagged_stream_0_1_0_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 2, "packet_len")
        self.blocks_stream_to_tagged_stream_0_1_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 2, "packet_len")
        self.blocks_stream_to_tagged_stream_0_1 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 2, "packet_len")
        self.blocks_stream_to_tagged_stream_0_0_0_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 380, "packet_len")
        self.blocks_stream_to_tagged_stream_0_0_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 252, "packet_len")
        self.blocks_stream_to_tagged_stream_0_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 124, "packet_len")
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 60, "packet_len")
        self.blocks_selector_0_0 = blocks.selector(gr.sizeof_gr_complex*1,0,0)
        self.blocks_selector_0_0.set_enabled(True)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,0,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_repack_bits_bb_0_4_0_0_0 = blocks.repack_bits_bb(8, hdr_const.bits_per_symbol(), 'packet_len', False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0_4_0_0 = blocks.repack_bits_bb(8, hdr_const.bits_per_symbol(), 'packet_len', False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0_4_0 = blocks.repack_bits_bb(8, hdr_const.bits_per_symbol(), 'packet_len', False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0_4 = blocks.repack_bits_bb(8, hdr_const.bits_per_symbol(), 'packet_len', False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0_3_0 = blocks.repack_bits_bb(8, hdr_const.bits_per_symbol(), 'packet_len', False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0_3 = blocks.repack_bits_bb(8, hdr_const.bits_per_symbol(), 'packet_len', False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0_2 = blocks.repack_bits_bb(8, hdr_const.bits_per_symbol(), 'packet_len', False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0_1_1_0 = blocks.repack_bits_bb(pld_const_64qam.bits_per_symbol(), 8, "payload symbols", False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0_1_1 = blocks.repack_bits_bb(pld_const_16qam.bits_per_symbol(), 8, "payload symbols", False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0_1_0_0 = blocks.repack_bits_bb(hdr_const.bits_per_symbol(), 8, "payload symbols", False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0_1_0 = blocks.repack_bits_bb(hdr_const.bits_per_symbol(), 8, "payload symbols", False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0_1 = blocks.repack_bits_bb(pld_const_qpsk.bits_per_symbol(), 8, "payload symbols", False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0_0_2_0_0_0 = blocks.repack_bits_bb(8, hdr_const.bits_per_symbol(), 'packet_len', False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0_0_2_0_0 = blocks.repack_bits_bb(8, hdr_const.bits_per_symbol(), 'packet_len', False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0_0_2_0 = blocks.repack_bits_bb(8, hdr_const.bits_per_symbol(), 'packet_len', False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0_0_2 = blocks.repack_bits_bb(8, hdr_const.bits_per_symbol(), 'packet_len', False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0_0_1_0 = blocks.repack_bits_bb(8, pld_const_64qam.bits_per_symbol(), 'packet_len', False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0_0_1 = blocks.repack_bits_bb(8, pld_const_16qam.bits_per_symbol(), 'packet_len', False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0_0_0 = blocks.repack_bits_bb(8, hdr_const.bits_per_symbol(), 'packet_len', False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0_0 = blocks.repack_bits_bb(8, pld_const_qpsk.bits_per_symbol(), 'packet_len', False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(8, hdr_const.bits_per_symbol(), 'packet_len', False, gr.GR_MSB_FIRST)
        self.blocks_null_sink_0_1 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_0_1 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_0_0_0_1 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_0_0_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_0_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_0_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_multiply_const_vxx_0_0_2 = blocks.multiply_const_cc(0.5)
        self.blocks_multiply_const_vxx_0_0_1 = blocks.multiply_const_cc(scale_16QAM)
        self.blocks_multiply_const_vxx_0_0_0_0 = blocks.multiply_const_cc(1/scale_16QAM*1.118)
        self.blocks_multiply_const_vxx_0_0_0 = blocks.multiply_const_cc(1/scale_64QAM*1.15)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_cc(scale_64QAM)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(0.5)
        self.analog_random_source_x_1_0_0_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 256, 1000))), True)
        self.analog_random_source_x_1_0_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 256, 1000))), True)
        self.analog_random_source_x_1_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 256, 1000))), True)
        self.analog_random_source_x_1 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 256, 1000))), True)
        self.analog_random_source_x_0_0_0_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 256, 10000000))), True)
        self.analog_random_source_x_0_0_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 256, 10000000))), True)
        self.analog_random_source_x_0_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 256, 10000000))), True)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 256, 10000000))), True)
        self.TFMv5_tx_controller_0 = TFMv5.tx_controller()
        self.TFMv5_header_payload_demux_am_0 = TFMv5.header_payload_demux_am(
            (hdr_format_bpsk.header_nbits()) //  hdr_const.bits_per_symbol(),
            1,
            0,
            "payload symbols",
            "amp_est",
            True,
            gr.sizeof_gr_complex,
            "rx_time",
            1,
            [],
            0)
        self.TFMv5_energy_scale_0_0 = TFMv5.energy_scale(1, samp_rate, 12)
        self.TFMv5_energy_scale_0 = TFMv5.energy_scale(1, samp_rate*2, 1)
        self.TFMv5_dispersion_probe_0_1_0_0_0_0_0 = TFMv5.dispersion_probe(3, samp_rate/2, 0, 0.02, 0.03, 0.04, 0.05,0.06,0.07)
        self.TFMv5_dispersion_probe_0_1_0_0_0_0 = TFMv5.dispersion_probe(2, samp_rate/2, 0, 0.02, 0.03, 0.04, 0.05,0.06,0.07)
        self.TFMv5_dispersion_probe_0_1_0_0_0 = TFMv5.dispersion_probe(1, samp_rate/2, 0, 0.02, 0.03, 0.04, 0.05,0.06,0.07)
        self.TFMv5_dispersion_probe_0_1_0_0 = TFMv5.dispersion_probe(0, samp_rate/2, 0, 0.02, 0.03, 0.04, 0.05,0.06,0.07)
        self.TFMv5_crc32_check_0 = TFMv5.crc32_check(2000,0,0,0.9)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.TFMv5_crc32_check_0, 'out_state'), (self.blocks_selector_0_0, 'iindex'))
        self.msg_connect((self.TFMv5_dispersion_probe_0_1_0_0, 'threshold'), (self.TFMv5_crc32_check_0, 'in_state'))
        self.msg_connect((self.TFMv5_dispersion_probe_0_1_0_0_0, 'threshold'), (self.TFMv5_crc32_check_0, 'in_state'))
        self.msg_connect((self.TFMv5_dispersion_probe_0_1_0_0_0_0, 'threshold'), (self.TFMv5_crc32_check_0, 'in_state'))
        self.msg_connect((self.TFMv5_dispersion_probe_0_1_0_0_0_0_0, 'threshold'), (self.TFMv5_crc32_check_0, 'in_state'))
        self.msg_connect((self.TFMv5_tx_controller_0, 'index'), (self.blocks_selector_0, 'iindex'))
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), (self.TFMv5_crc32_check_0, 'in'))
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0_0, 'pdus'), (self.TFMv5_crc32_check_0, 'in'))
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0_0_0, 'pdus'), (self.digital_crc32_async_bb_0_0_0, 'in'))
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0_1, 'pdus'), (self.TFMv5_crc32_check_0, 'in'))
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0_1_0, 'pdus'), (self.TFMv5_crc32_check_0, 'in'))
        self.msg_connect((self.digital_crc32_async_bb_0_0_0, 'out'), (self.TFMv5_tx_controller_0, 'state'))
        self.msg_connect((self.digital_protocol_parser_b_0, 'info'), (self.TFMv5_header_payload_demux_am_0, 'header_data'))
        self.msg_connect((self.digital_protocol_parser_b_0_0, 'info'), (self.digital_header_payload_demux_0, 'header_data'))
        self.connect((self.TFMv5_energy_scale_0, 0), (self.digital_fll_band_edge_cc_0, 0))
        self.connect((self.TFMv5_energy_scale_0_0, 0), (self.digital_fll_band_edge_cc_0_0, 0))
        self.connect((self.TFMv5_header_payload_demux_am_0, 4), (self.blocks_multiply_const_vxx_0_0_0, 0))
        self.connect((self.TFMv5_header_payload_demux_am_0, 3), (self.blocks_multiply_const_vxx_0_0_0_0, 0))
        self.connect((self.TFMv5_header_payload_demux_am_0, 0), (self.digital_cma_equalizer_cc_0_0_0_0, 0))
        self.connect((self.TFMv5_header_payload_demux_am_0, 1), (self.digital_cma_equalizer_cc_0_0_0_0_0, 0))
        self.connect((self.TFMv5_header_payload_demux_am_0, 2), (self.digital_cma_equalizer_cc_0_0_0_0_0_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.analog_random_source_x_0_0, 0), (self.blocks_stream_to_tagged_stream_0_0, 0))
        self.connect((self.analog_random_source_x_0_0_0, 0), (self.blocks_stream_to_tagged_stream_0_0_0, 0))
        self.connect((self.analog_random_source_x_0_0_0_0, 0), (self.blocks_stream_to_tagged_stream_0_0_0_0, 0))
        self.connect((self.analog_random_source_x_1, 0), (self.blocks_stream_to_tagged_stream_0_1_2, 0))
        self.connect((self.analog_random_source_x_1_0, 0), (self.blocks_stream_to_tagged_stream_0_1_2_0, 0))
        self.connect((self.analog_random_source_x_1_0_0, 0), (self.blocks_stream_to_tagged_stream_0_1_2_0_0, 0))
        self.connect((self.analog_random_source_x_1_0_0_0, 0), (self.blocks_stream_to_tagged_stream_0_1_2_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_tagged_stream_mux_0_1_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0_0_0, 0), (self.digital_cma_equalizer_cc_0_0_0_1_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0_0_0, 0), (self.digital_lms_dd_equalizer_cc_2_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0_1, 0), (self.blocks_tagged_stream_mux_0_1, 1))
        self.connect((self.blocks_multiply_const_vxx_0_0_2, 0), (self.uhd_usrp_sink_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_diff_encoder_bb_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_0, 0), (self.digital_diff_encoder_bb_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_0_0, 0), (self.digital_diff_encoder_bb_0_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_0_1, 0), (self.digital_diff_encoder_bb_0_0_1, 0))
        self.connect((self.blocks_repack_bits_bb_0_0_1_0, 0), (self.digital_diff_encoder_bb_0_0_1_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_0_2, 0), (self.digital_diff_encoder_bb_0_0_2, 0))
        self.connect((self.blocks_repack_bits_bb_0_0_2_0, 0), (self.digital_diff_encoder_bb_0_0_2_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_0_2_0_0, 0), (self.digital_diff_encoder_bb_0_0_2_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_0_2_0_0_0, 0), (self.digital_diff_encoder_bb_0_0_2_0_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_1, 0), (self.blocks_tagged_stream_to_pdu_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_1_0, 0), (self.blocks_tagged_stream_to_pdu_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_1_0_0, 0), (self.blocks_tagged_stream_to_pdu_0_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_1_1, 0), (self.blocks_tagged_stream_to_pdu_0_1, 0))
        self.connect((self.blocks_repack_bits_bb_0_1_1_0, 0), (self.blocks_tagged_stream_to_pdu_0_1_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_2, 0), (self.digital_diff_encoder_bb_0_1, 0))
        self.connect((self.blocks_repack_bits_bb_0_3, 0), (self.digital_diff_encoder_bb_0_2, 0))
        self.connect((self.blocks_repack_bits_bb_0_3_0, 0), (self.digital_diff_encoder_bb_0_2_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_4, 0), (self.digital_diff_encoder_bb_0_3, 0))
        self.connect((self.blocks_repack_bits_bb_0_4_0, 0), (self.digital_diff_encoder_bb_0_3_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_4_0_0, 0), (self.digital_diff_encoder_bb_0_3_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_4_0_0_0, 0), (self.digital_diff_encoder_bb_0_3_0_0_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.blocks_selector_0_0, 0), (self.channels_channel_model_0_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.digital_crc32_bb_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0_0, 0), (self.digital_crc32_bb_0_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0_0_0, 0), (self.digital_crc32_bb_0_0_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0_0_0_0, 0), (self.digital_crc32_bb_0_0_0_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0_1, 0), (self.blocks_tagged_stream_mux_0_2_2, 1))
        self.connect((self.blocks_stream_to_tagged_stream_0_1_0, 0), (self.blocks_tagged_stream_mux_0_2_2_0, 1))
        self.connect((self.blocks_stream_to_tagged_stream_0_1_0_0, 0), (self.blocks_tagged_stream_mux_0_2_2_0_0, 1))
        self.connect((self.blocks_stream_to_tagged_stream_0_1_0_0_0, 0), (self.blocks_tagged_stream_mux_0_2_2_0_0_0, 1))
        self.connect((self.blocks_stream_to_tagged_stream_0_1_2, 0), (self.blocks_tagged_stream_mux_0_2_2, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0_1_2_0, 0), (self.blocks_tagged_stream_mux_0_2_2_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0_1_2_0_0, 0), (self.blocks_tagged_stream_mux_0_2_2_0_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0_1_2_0_0_0, 0), (self.blocks_tagged_stream_mux_0_2_2_0_0_0, 0))
        self.connect((self.blocks_tag_gate_0_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.blocks_tag_gate_0_0_0, 0), (self.digital_pfb_clock_sync_xxx_0_0, 0))
        self.connect((self.blocks_tagged_stream_multiply_length_0_0, 0), (self.pfb_arb_resampler_xxx_0_0, 0))
        self.connect((self.blocks_tagged_stream_multiply_length_0_0_0, 0), (self.pfb_arb_resampler_xxx_0_0_0, 0))
        self.connect((self.blocks_tagged_stream_multiply_length_0_0_0_0, 0), (self.pfb_arb_resampler_xxx_0_0_0_0, 0))
        self.connect((self.blocks_tagged_stream_multiply_length_0_0_0_0_0, 0), (self.pfb_arb_resampler_xxx_0_0_0_0_0, 0))
        self.connect((self.blocks_tagged_stream_multiply_length_0_0_0_0_0_0, 0), (self.pfb_arb_resampler_xxx_0_0_0_0_0_0, 0))
        self.connect((self.blocks_tagged_stream_multiply_length_0_0_0_0_0_0_0, 0), (self.pfb_arb_resampler_xxx_0_0_0_0_0_0_0, 0))
        self.connect((self.blocks_tagged_stream_multiply_length_0_0_0_1, 0), (self.pfb_arb_resampler_xxx_0_0_0_1, 0))
        self.connect((self.blocks_tagged_stream_multiply_length_0_0_1, 0), (self.pfb_arb_resampler_xxx_0_0_1, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.blocks_tagged_stream_multiply_length_0_0_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0_0, 0), (self.blocks_tagged_stream_multiply_length_0_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0_1, 0), (self.blocks_tagged_stream_multiply_length_0_0_0_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0_1_0, 0), (self.blocks_tagged_stream_multiply_length_0_0_0_0_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0_2, 0), (self.blocks_tagged_stream_multiply_length_0_0_1, 0))
        self.connect((self.blocks_tagged_stream_mux_0_2_0, 0), (self.blocks_tagged_stream_multiply_length_0_0_0_1, 0))
        self.connect((self.blocks_tagged_stream_mux_0_2_0_0, 0), (self.blocks_tagged_stream_multiply_length_0_0_0_0_0_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0_2_0_0_0, 0), (self.blocks_tagged_stream_multiply_length_0_0_0_0_0_0_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0_2_2, 0), (self.digital_crc32_bb_0_1, 0))
        self.connect((self.blocks_tagged_stream_mux_0_2_2_0, 0), (self.digital_crc32_bb_0_1_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0_2_2_0_0, 0), (self.digital_crc32_bb_0_1_0_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0_2_2_0_0_0, 0), (self.digital_crc32_bb_0_1_0_0_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_stream_to_tagged_stream_0_1, 0))
        self.connect((self.blocks_vector_source_x_0_0, 0), (self.blocks_stream_to_tagged_stream_0_1_0, 0))
        self.connect((self.blocks_vector_source_x_0_0_0, 0), (self.blocks_stream_to_tagged_stream_0_1_0_0, 0))
        self.connect((self.blocks_vector_source_x_0_0_0_0, 0), (self.blocks_stream_to_tagged_stream_0_1_0_0_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.channels_channel_model_0_0, 0), (self.blocks_multiply_const_vxx_0_0_2, 0))
        self.connect((self.channels_channel_model_0_0, 0), (self.qtgui_time_sink_x_0_2, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.digital_chunks_to_symbols_xx_0_0_0, 0), (self.blocks_tagged_stream_mux_0_0, 1))
        self.connect((self.digital_chunks_to_symbols_xx_0_0_1, 0), (self.blocks_multiply_const_vxx_0_0_1, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0_1_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0_2, 0), (self.blocks_tagged_stream_mux_0_2, 1))
        self.connect((self.digital_chunks_to_symbols_xx_0_0_2_0, 0), (self.blocks_tagged_stream_mux_0_2_0, 1))
        self.connect((self.digital_chunks_to_symbols_xx_0_0_2_0_0, 0), (self.blocks_tagged_stream_mux_0_2_0_0, 1))
        self.connect((self.digital_chunks_to_symbols_xx_0_0_2_0_0_0, 0), (self.blocks_tagged_stream_mux_0_2_0_0_0, 1))
        self.connect((self.digital_chunks_to_symbols_xx_0_1, 0), (self.blocks_tagged_stream_mux_0_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_2, 0), (self.blocks_tagged_stream_mux_0_1, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_2_0, 0), (self.blocks_tagged_stream_mux_0_1_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_3, 0), (self.blocks_tagged_stream_mux_0_2, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_3_0, 0), (self.blocks_tagged_stream_mux_0_2_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_3_0_0, 0), (self.blocks_tagged_stream_mux_0_2_0_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_3_0_0_0, 0), (self.blocks_tagged_stream_mux_0_2_0_0_0, 0))
        self.connect((self.digital_cma_equalizer_cc_0_0_0, 0), (self.TFMv5_header_payload_demux_am_0, 0))
        self.connect((self.digital_cma_equalizer_cc_0_0_0_0, 0), (self.digital_costas_loop_cc_0_0, 0))
        self.connect((self.digital_cma_equalizer_cc_0_0_0_0_0, 0), (self.digital_costas_loop_cc_0_0_0_0, 0))
        self.connect((self.digital_cma_equalizer_cc_0_0_0_0_0_0, 0), (self.digital_costas_loop_cc_0_0_0, 0))
        self.connect((self.digital_cma_equalizer_cc_0_0_0_1, 0), (self.digital_header_payload_demux_0, 0))
        self.connect((self.digital_cma_equalizer_cc_0_0_0_1_0, 0), (self.digital_lms_dd_equalizer_cc_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_diff_decoder_bb_0_0_0_2_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0, 0), (self.digital_diff_decoder_bb_0_0_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0_0, 0), (self.digital_diff_decoder_bb_0_0_0_1, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0_0_0, 0), (self.digital_diff_decoder_bb_0_0_0_1_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0_1, 0), (self.digital_diff_decoder_bb_0_0_0_2, 0))
        self.connect((self.digital_constellation_receiver_cb_0, 4), (self.TFMv5_dispersion_probe_0_1_0_0_0_0, 0))
        self.connect((self.digital_constellation_receiver_cb_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.digital_constellation_receiver_cb_0, 1), (self.blocks_null_sink_0_0, 0))
        self.connect((self.digital_constellation_receiver_cb_0, 2), (self.blocks_null_sink_0_0_0, 0))
        self.connect((self.digital_constellation_receiver_cb_0, 3), (self.blocks_null_sink_0_0_0_0, 0))
        self.connect((self.digital_constellation_receiver_cb_0, 4), (self.digital_constellation_decoder_cb_0_0_1, 0))
        self.connect((self.digital_constellation_receiver_cb_0, 4), (self.qtgui_const_sink_x_0_0_1, 0))
        self.connect((self.digital_constellation_receiver_cb_0_0, 4), (self.TFMv5_dispersion_probe_0_1_0_0_0_0_0, 0))
        self.connect((self.digital_constellation_receiver_cb_0_0, 3), (self.blocks_null_sink_0_0_0_0_0, 0))
        self.connect((self.digital_constellation_receiver_cb_0_0, 2), (self.blocks_null_sink_0_0_0_1, 0))
        self.connect((self.digital_constellation_receiver_cb_0_0, 1), (self.blocks_null_sink_0_0_1, 0))
        self.connect((self.digital_constellation_receiver_cb_0_0, 0), (self.blocks_null_sink_0_1, 0))
        self.connect((self.digital_constellation_receiver_cb_0_0, 4), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.digital_constellation_receiver_cb_0_0, 4), (self.qtgui_const_sink_x_0_0_1_0, 0))
        self.connect((self.digital_constellation_soft_decoder_cf_0_0, 0), (self.fec_generic_decoder_0_0, 0))
        self.connect((self.digital_constellation_soft_decoder_cf_0_0_0, 0), (self.fec_generic_decoder_0_0_0, 0))
        self.connect((self.digital_corr_est_cc_0, 0), (self.blocks_tag_gate_0_0, 0))
        self.connect((self.digital_corr_est_cc_0_0, 0), (self.blocks_tag_gate_0_0_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0, 0), (self.digital_constellation_soft_decoder_cf_0_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0_0, 0), (self.TFMv5_dispersion_probe_0_1_0_0_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0_0, 0), (self.digital_constellation_decoder_cb_0_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0_0, 0), (self.qtgui_const_sink_x_0_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0_0_0, 0), (self.TFMv5_dispersion_probe_0_1_0_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0_0_0, 0), (self.digital_constellation_decoder_cb_0_0_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0_0_0, 0), (self.qtgui_const_sink_x_0_0_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0_0_0_0, 0), (self.digital_constellation_decoder_cb_0_0_0_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0_0_0_0, 0), (self.qtgui_const_sink_x_0_0_0_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0_1, 0), (self.digital_constellation_soft_decoder_cf_0_0_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0_1, 0), (self.qtgui_const_sink_x_0_1, 0))
        self.connect((self.digital_crc32_bb_0, 0), (self.blocks_repack_bits_bb_0_0_0, 0))
        self.connect((self.digital_crc32_bb_0, 0), (self.digital_protocol_formatter_bb_0_0, 0))
        self.connect((self.digital_crc32_bb_0_0, 0), (self.blocks_repack_bits_bb_0_0, 0))
        self.connect((self.digital_crc32_bb_0_0, 0), (self.digital_protocol_formatter_bb_0, 0))
        self.connect((self.digital_crc32_bb_0_0_0, 0), (self.blocks_repack_bits_bb_0_0_1, 0))
        self.connect((self.digital_crc32_bb_0_0_0, 0), (self.digital_protocol_formatter_bb_0_0_0, 0))
        self.connect((self.digital_crc32_bb_0_0_0_0, 0), (self.blocks_repack_bits_bb_0_0_1_0, 0))
        self.connect((self.digital_crc32_bb_0_0_0_0, 0), (self.digital_protocol_formatter_bb_0_0_0_0, 0))
        self.connect((self.digital_crc32_bb_0_1, 0), (self.blocks_repack_bits_bb_0_0_2, 0))
        self.connect((self.digital_crc32_bb_0_1, 0), (self.digital_protocol_formatter_bb_0_1, 0))
        self.connect((self.digital_crc32_bb_0_1_0, 0), (self.blocks_repack_bits_bb_0_0_2_0, 0))
        self.connect((self.digital_crc32_bb_0_1_0, 0), (self.digital_protocol_formatter_bb_0_1_0, 0))
        self.connect((self.digital_crc32_bb_0_1_0_0, 0), (self.blocks_repack_bits_bb_0_0_2_0_0, 0))
        self.connect((self.digital_crc32_bb_0_1_0_0, 0), (self.digital_protocol_formatter_bb_0_1_0_0, 0))
        self.connect((self.digital_crc32_bb_0_1_0_0_0, 0), (self.blocks_repack_bits_bb_0_0_2_0_0_0, 0))
        self.connect((self.digital_crc32_bb_0_1_0_0_0, 0), (self.digital_protocol_formatter_bb_0_1_0_0_0, 0))
        self.connect((self.digital_diff_decoder_bb_0_0_0, 0), (self.blocks_repack_bits_bb_0_1, 0))
        self.connect((self.digital_diff_decoder_bb_0_0_0_0, 0), (self.digital_protocol_parser_b_0, 0))
        self.connect((self.digital_diff_decoder_bb_0_0_0_0_0, 0), (self.digital_protocol_parser_b_0_0, 0))
        self.connect((self.digital_diff_decoder_bb_0_0_0_1, 0), (self.blocks_repack_bits_bb_0_1_0, 0))
        self.connect((self.digital_diff_decoder_bb_0_0_0_1_0, 0), (self.blocks_repack_bits_bb_0_1_0_0, 0))
        self.connect((self.digital_diff_decoder_bb_0_0_0_2, 0), (self.blocks_repack_bits_bb_0_1_1, 0))
        self.connect((self.digital_diff_decoder_bb_0_0_0_2_0, 0), (self.blocks_repack_bits_bb_0_1_1_0, 0))
        self.connect((self.digital_diff_encoder_bb_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.digital_diff_encoder_bb_0_0, 0), (self.digital_chunks_to_symbols_xx_0_0, 0))
        self.connect((self.digital_diff_encoder_bb_0_0_0, 0), (self.digital_chunks_to_symbols_xx_0_0_0, 0))
        self.connect((self.digital_diff_encoder_bb_0_0_1, 0), (self.digital_chunks_to_symbols_xx_0_0_1, 0))
        self.connect((self.digital_diff_encoder_bb_0_0_1_0, 0), (self.digital_chunks_to_symbols_xx_0_0_1_0, 0))
        self.connect((self.digital_diff_encoder_bb_0_0_2, 0), (self.digital_chunks_to_symbols_xx_0_0_2, 0))
        self.connect((self.digital_diff_encoder_bb_0_0_2_0, 0), (self.digital_chunks_to_symbols_xx_0_0_2_0, 0))
        self.connect((self.digital_diff_encoder_bb_0_0_2_0_0, 0), (self.digital_chunks_to_symbols_xx_0_0_2_0_0, 0))
        self.connect((self.digital_diff_encoder_bb_0_0_2_0_0_0, 0), (self.digital_chunks_to_symbols_xx_0_0_2_0_0_0, 0))
        self.connect((self.digital_diff_encoder_bb_0_1, 0), (self.digital_chunks_to_symbols_xx_0_1, 0))
        self.connect((self.digital_diff_encoder_bb_0_2, 0), (self.digital_chunks_to_symbols_xx_0_2, 0))
        self.connect((self.digital_diff_encoder_bb_0_2_0, 0), (self.digital_chunks_to_symbols_xx_0_2_0, 0))
        self.connect((self.digital_diff_encoder_bb_0_3, 0), (self.digital_chunks_to_symbols_xx_0_3, 0))
        self.connect((self.digital_diff_encoder_bb_0_3_0, 0), (self.digital_chunks_to_symbols_xx_0_3_0, 0))
        self.connect((self.digital_diff_encoder_bb_0_3_0_0, 0), (self.digital_chunks_to_symbols_xx_0_3_0_0, 0))
        self.connect((self.digital_diff_encoder_bb_0_3_0_0_0, 0), (self.digital_chunks_to_symbols_xx_0_3_0_0_0, 0))
        self.connect((self.digital_fll_band_edge_cc_0, 0), (self.digital_corr_est_cc_0, 0))
        self.connect((self.digital_fll_band_edge_cc_0_0, 0), (self.digital_corr_est_cc_0_0, 0))
        self.connect((self.digital_header_payload_demux_0, 1), (self.digital_costas_loop_cc_0_0_0_0_0, 0))
        self.connect((self.digital_header_payload_demux_0, 0), (self.digital_costas_loop_cc_0_0_1, 0))
        self.connect((self.digital_lms_dd_equalizer_cc_0, 0), (self.digital_constellation_receiver_cb_0_0, 0))
        self.connect((self.digital_lms_dd_equalizer_cc_2_0_0_0, 0), (self.digital_constellation_receiver_cb_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_cma_equalizer_cc_0_0_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0_0, 0), (self.digital_cma_equalizer_cc_0_0_0_1, 0))
        self.connect((self.digital_protocol_formatter_bb_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.digital_protocol_formatter_bb_0_0, 0), (self.blocks_repack_bits_bb_0_2, 0))
        self.connect((self.digital_protocol_formatter_bb_0_0_0, 0), (self.blocks_repack_bits_bb_0_3, 0))
        self.connect((self.digital_protocol_formatter_bb_0_0_0_0, 0), (self.blocks_repack_bits_bb_0_3_0, 0))
        self.connect((self.digital_protocol_formatter_bb_0_1, 0), (self.blocks_repack_bits_bb_0_4, 0))
        self.connect((self.digital_protocol_formatter_bb_0_1_0, 0), (self.blocks_repack_bits_bb_0_4_0, 0))
        self.connect((self.digital_protocol_formatter_bb_0_1_0_0, 0), (self.blocks_repack_bits_bb_0_4_0_0, 0))
        self.connect((self.digital_protocol_formatter_bb_0_1_0_0_0, 0), (self.blocks_repack_bits_bb_0_4_0_0_0, 0))
        self.connect((self.fec_generic_decoder_0_0, 0), (self.digital_diff_decoder_bb_0_0_0_0, 0))
        self.connect((self.fec_generic_decoder_0_0_0, 0), (self.digital_diff_decoder_bb_0_0_0_0_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0_0_0, 0), (self.blocks_selector_0, 1))
        self.connect((self.pfb_arb_resampler_xxx_0_0_0_0, 0), (self.blocks_selector_0, 2))
        self.connect((self.pfb_arb_resampler_xxx_0_0_0_0_0, 0), (self.blocks_selector_0, 3))
        self.connect((self.pfb_arb_resampler_xxx_0_0_0_0_0_0, 0), (self.blocks_selector_0_0, 2))
        self.connect((self.pfb_arb_resampler_xxx_0_0_0_0_0_0_0, 0), (self.blocks_selector_0_0, 3))
        self.connect((self.pfb_arb_resampler_xxx_0_0_0_1, 0), (self.blocks_selector_0_0, 1))
        self.connect((self.pfb_arb_resampler_xxx_0_0_1, 0), (self.blocks_selector_0_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.TFMv5_energy_scale_0, 0))
        self.connect((self.uhd_usrp_source_0_0, 0), (self.TFMv5_energy_scale_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Aplicacion_Final")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_hdr_const(self):
        return self.hdr_const

    def set_hdr_const(self, hdr_const):
        self.hdr_const = hdr_const
        self.set_rxmod(digital.generic_mod(self.hdr_const, True, self.sps, True, self.eb, False, False))

    def get_hdr_format(self):
        return self.hdr_format

    def set_hdr_format(self, hdr_format):
        self.hdr_format = hdr_format

    def get_hdr_format_16qam(self):
        return self.hdr_format_16qam

    def set_hdr_format_16qam(self, hdr_format_16qam):
        self.hdr_format_16qam = hdr_format_16qam

    def get_hdr_format_64qam(self):
        return self.hdr_format_64qam

    def set_hdr_format_64qam(self, hdr_format_64qam):
        self.hdr_format_64qam = hdr_format_64qam

    def get_hdr_format_bpsk(self):
        return self.hdr_format_bpsk

    def set_hdr_format_bpsk(self, hdr_format_bpsk):
        self.hdr_format_bpsk = hdr_format_bpsk

    def get_hdr_format_bpsk_copy(self):
        return self.hdr_format_bpsk_copy

    def set_hdr_format_bpsk_copy(self, hdr_format_bpsk_copy):
        self.hdr_format_bpsk_copy = hdr_format_bpsk_copy

    def get_hdr_format_qpsk(self):
        return self.hdr_format_qpsk

    def set_hdr_format_qpsk(self, hdr_format_qpsk):
        self.hdr_format_qpsk = hdr_format_qpsk

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_psf_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0, self.eb, 15*self.sps*self.nfilts))
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.eb, 11*self.sps*self.nfilts))
        self.set_rxmod(digital.generic_mod(self.hdr_const, True, self.sps, True, self.eb, False, False))
        self.blocks_tagged_stream_multiply_length_0_0.set_scalar(self.sps)
        self.blocks_tagged_stream_multiply_length_0_0_0.set_scalar(self.sps)
        self.blocks_tagged_stream_multiply_length_0_0_0_0.set_scalar(self.sps)
        self.blocks_tagged_stream_multiply_length_0_0_0_0_0.set_scalar(self.sps)
        self.blocks_tagged_stream_multiply_length_0_0_0_0_0_0.set_scalar(self.sps)
        self.blocks_tagged_stream_multiply_length_0_0_0_0_0_0_0.set_scalar(self.sps)
        self.blocks_tagged_stream_multiply_length_0_0_0_1.set_scalar(self.sps)
        self.blocks_tagged_stream_multiply_length_0_0_1.set_scalar(self.sps)
        self.pfb_arb_resampler_xxx_0_0.set_rate(self.sps)
        self.pfb_arb_resampler_xxx_0_0_0.set_rate(self.sps)
        self.pfb_arb_resampler_xxx_0_0_0_0.set_rate(self.sps)
        self.pfb_arb_resampler_xxx_0_0_0_0_0.set_rate(self.sps)
        self.pfb_arb_resampler_xxx_0_0_0_0_0_0.set_rate(self.sps)
        self.pfb_arb_resampler_xxx_0_0_0_0_0_0_0.set_rate(self.sps)
        self.pfb_arb_resampler_xxx_0_0_0_1.set_rate(self.sps)
        self.pfb_arb_resampler_xxx_0_0_1.set_rate(self.sps)

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_psf_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0, self.eb, 15*self.sps*self.nfilts))
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.eb, 11*self.sps*self.nfilts))
        self.set_taps_per_filt(int(len(self.psf_taps)/self.nfilts))

    def get_eb(self):
        return self.eb

    def set_eb(self, eb):
        self.eb = eb
        self.set_psf_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0, self.eb, 15*self.sps*self.nfilts))
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.eb, 11*self.sps*self.nfilts))
        self.set_rxmod(digital.generic_mod(self.hdr_const, True, self.sps, True, self.eb, False, False))

    def get_psf_taps(self):
        return self.psf_taps

    def set_psf_taps(self, psf_taps):
        self.psf_taps = psf_taps
        self.set_taps_per_filt(int(len(self.psf_taps)/self.nfilts))
        self.pfb_arb_resampler_xxx_0_0.set_taps(self.psf_taps)
        self.pfb_arb_resampler_xxx_0_0_0.set_taps(self.psf_taps)
        self.pfb_arb_resampler_xxx_0_0_0_0.set_taps(self.psf_taps)
        self.pfb_arb_resampler_xxx_0_0_0_0_0.set_taps(self.psf_taps)
        self.pfb_arb_resampler_xxx_0_0_0_0_0_0.set_taps(self.psf_taps)
        self.pfb_arb_resampler_xxx_0_0_0_0_0_0_0.set_taps(self.psf_taps)
        self.pfb_arb_resampler_xxx_0_0_0_1.set_taps(self.psf_taps)
        self.pfb_arb_resampler_xxx_0_0_1.set_taps(self.psf_taps)

    def get_taps_per_filt(self):
        return self.taps_per_filt

    def set_taps_per_filt(self, taps_per_filt):
        self.taps_per_filt = taps_per_filt
        self.set_filt_delay(int(1+(self.taps_per_filt-1)//2))

    def get_rxmod(self):
        return self.rxmod

    def set_rxmod(self, rxmod):
        self.rxmod = rxmod

    def get_preamble(self):
        return self.preamble

    def set_preamble(self, preamble):
        self.preamble = preamble

    def get_d(self):
        return self.d

    def set_d(self, d):
        self.d = d

    def get_timing_loop_bw(self):
        return self.timing_loop_bw

    def set_timing_loop_bw(self, timing_loop_bw):
        self.timing_loop_bw = timing_loop_bw
        self.digital_pfb_clock_sync_xxx_0.set_loop_bandwidth(self.timing_loop_bw*2)
        self.digital_pfb_clock_sync_xxx_0_0.set_loop_bandwidth(self.timing_loop_bw*2)

    def get_taps(self):
        return self.taps

    def set_taps(self, taps):
        self.taps = taps

    def get_scale_64QAM(self):
        return self.scale_64QAM

    def set_scale_64QAM(self, scale_64QAM):
        self.scale_64QAM = scale_64QAM
        self.blocks_multiply_const_vxx_0_0.set_k(self.scale_64QAM)
        self.blocks_multiply_const_vxx_0_0_0.set_k(1/self.scale_64QAM*1.15)

    def get_scale_16QAM(self):
        return self.scale_16QAM

    def set_scale_16QAM(self, scale_16QAM):
        self.scale_16QAM = scale_16QAM
        self.blocks_multiply_const_vxx_0_0_0_0.set_k(1/self.scale_16QAM*1.118)
        self.blocks_multiply_const_vxx_0_0_1.set_k(self.scale_16QAM)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0_0.set_samp_rate(self.samp_rate/4)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0_0.set_samp_rate(self.samp_rate/4)

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.digital_pfb_clock_sync_xxx_0.update_taps(self.rrc_taps)
        self.digital_pfb_clock_sync_xxx_0_0.update_taps(self.rrc_taps)

    def get_pld_const_qpsk(self):
        return self.pld_const_qpsk

    def set_pld_const_qpsk(self, pld_const_qpsk):
        self.pld_const_qpsk = pld_const_qpsk

    def get_pld_const_64qam(self):
        return self.pld_const_64qam

    def set_pld_const_64qam(self, pld_const_64qam):
        self.pld_const_64qam = pld_const_64qam

    def get_pld_const_16qam(self):
        return self.pld_const_16qam

    def set_pld_const_16qam(self, pld_const_16qam):
        self.pld_const_16qam = pld_const_16qam

    def get_noise_volt(self):
        return self.noise_volt

    def set_noise_volt(self, noise_volt):
        self.noise_volt = noise_volt
        self.channels_channel_model_0.set_noise_voltage(self.noise_volt)
        self.channels_channel_model_0_0.set_noise_voltage(self.noise_volt)

    def get_modulated_sync_word(self):
        return self.modulated_sync_word

    def set_modulated_sync_word(self, modulated_sync_word):
        self.modulated_sync_word = modulated_sync_word

    def get_mark_delay(self):
        return self.mark_delay

    def set_mark_delay(self, mark_delay):
        self.mark_delay = mark_delay
        self.digital_corr_est_cc_0.set_mark_delay(self.mark_delay)
        self.digital_corr_est_cc_0_0.set_mark_delay(self.mark_delay)

    def get_gain_tx(self):
        return self.gain_tx

    def set_gain_tx(self, gain_tx):
        self.gain_tx = gain_tx
        self.uhd_usrp_sink_0.set_gain(self.gain_tx, 0)

    def get_gain_rx(self):
        return self.gain_rx

    def set_gain_rx(self, gain_rx):
        self.gain_rx = gain_rx
        self.uhd_usrp_sink_0_0.set_gain(self.gain_rx, 0)
        self.uhd_usrp_source_0.set_gain(self.gain_rx, 0)
        self.uhd_usrp_source_0_0.set_gain(self.gain_rx, 0)

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset
        self.channels_channel_model_0.set_frequency_offset(self.freq_offset)
        self.channels_channel_model_0_0.set_frequency_offset(self.freq_offset)

    def get_freq2(self):
        return self.freq2

    def set_freq2(self, freq2):
        self.freq2 = freq2
        self.uhd_usrp_sink_0_0.set_center_freq(self.freq2, 0)
        self.uhd_usrp_source_0_0.set_center_freq(self.freq2, 0)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_sink_0.set_center_freq(self.freq, 0)
        self.uhd_usrp_source_0.set_center_freq(self.freq, 0)

    def get_filt_delay(self):
        return self.filt_delay

    def set_filt_delay(self, filt_delay):
        self.filt_delay = filt_delay

    def get_dec_dummy_0(self):
        return self.dec_dummy_0

    def set_dec_dummy_0(self, dec_dummy_0):
        self.dec_dummy_0 = dec_dummy_0

    def get_dec_dummy(self):
        return self.dec_dummy

    def set_dec_dummy(self, dec_dummy):
        self.dec_dummy = dec_dummy



def argument_parser():
    parser = ArgumentParser()
    return parser


def main(top_block_cls=Aplicacion_Final, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
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
