#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: radiofreeurth
# GNU Radio version: 3.10.11.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import analog
import math
from gnuradio import audio
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
import osmosdr
import time
import sip
import threading



class signalAnalysis_1(gr.top_block, Qt.QWidget):

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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "signalAnalysis_1")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.vol = vol = 0
        self.samp_rate = samp_rate = 8e6
        self.gain = gain = 0
        self.demodSelect = demodSelect = 0
        self.cfshift = cfshift = 0
        self.cf = cf = 101.3
        self.bw = bw = 20e3

        ##################################################
        # Blocks
        ##################################################

        self.mt = Qt.QTabWidget()
        self.mt_widget_0 = Qt.QWidget()
        self.mt_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.mt_widget_0)
        self.mt_grid_layout_0 = Qt.QGridLayout()
        self.mt_layout_0.addLayout(self.mt_grid_layout_0)
        self.mt.addTab(self.mt_widget_0, 'RF')
        self.mt_widget_1 = Qt.QWidget()
        self.mt_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.mt_widget_1)
        self.mt_grid_layout_1 = Qt.QGridLayout()
        self.mt_layout_1.addLayout(self.mt_grid_layout_1)
        self.mt.addTab(self.mt_widget_1, 'Constellation')
        self.mt_widget_2 = Qt.QWidget()
        self.mt_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.mt_widget_2)
        self.mt_grid_layout_2 = Qt.QGridLayout()
        self.mt_layout_2.addLayout(self.mt_grid_layout_2)
        self.mt.addTab(self.mt_widget_2, 'Zoomed Spectrum')
        self.mt_widget_3 = Qt.QWidget()
        self.mt_layout_3 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.mt_widget_3)
        self.mt_grid_layout_3 = Qt.QGridLayout()
        self.mt_layout_3.addLayout(self.mt_grid_layout_3)
        self.mt.addTab(self.mt_widget_3, 'Demod Selection')
        self.mt_widget_4 = Qt.QWidget()
        self.mt_layout_4 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.mt_widget_4)
        self.mt_grid_layout_4 = Qt.QGridLayout()
        self.mt_layout_4.addLayout(self.mt_grid_layout_4)
        self.mt.addTab(self.mt_widget_4, '')
        self.top_grid_layout.addWidget(self.mt, 2, 0, 20, 20)
        for r in range(2, 22):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 20):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._vol_range = qtgui.Range(-80, 50, 0.1, 0, 200)
        self._vol_win = qtgui.RangeWidget(self._vol_range, self.set_vol, "Volume (dB)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._vol_win, 1, 10, 1, 10)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(10, 20):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._gain_range = qtgui.Range(0, 31.5, 0.5, 0, 200)
        self._gain_win = qtgui.RangeWidget(self._gain_range, self.set_gain, "RF Gain (dB)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._gain_win, 0, 5, 1, 10)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(5, 15):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._demodSelect_options = [0, 1, 2, 3, 4]
        # Create the labels list
        self._demodSelect_labels = ['AM Full Carrier', 'AM-SC-SSB', 'AM-SC-DSB', 'FM', 'FM Double Demod']
        # Create the combo box
        # Create the radio buttons
        self._demodSelect_group_box = Qt.QGroupBox("Demod Selection" + ": ")
        self._demodSelect_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._demodSelect_button_group = variable_chooser_button_group()
        self._demodSelect_group_box.setLayout(self._demodSelect_box)
        for i, _label in enumerate(self._demodSelect_labels):
            radio_button = Qt.QRadioButton(_label)
            self._demodSelect_box.addWidget(radio_button)
            self._demodSelect_button_group.addButton(radio_button, i)
        self._demodSelect_callback = lambda i: Qt.QMetaObject.invokeMethod(self._demodSelect_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._demodSelect_options.index(i)))
        self._demodSelect_callback(self.demodSelect)
        self._demodSelect_button_group.buttonClicked[int].connect(
            lambda i: self.set_demodSelect(self._demodSelect_options[i]))
        self.mt_grid_layout_3.addWidget(self._demodSelect_group_box, 0, 0, 1, 10)
        for r in range(0, 1):
            self.mt_grid_layout_3.setRowStretch(r, 1)
        for c in range(0, 10):
            self.mt_grid_layout_3.setColumnStretch(c, 1)
        self._cfshift_range = qtgui.Range(-2000, 2000, 1, 0, 200)
        self._cfshift_win = qtgui.RangeWidget(self._cfshift_range, self.set_cfshift, "Center Freq Shift (Hz)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._cfshift_win, 1, 0, 1, 10)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 10):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._cf_tool_bar = Qt.QToolBar(self)
        self._cf_tool_bar.addWidget(Qt.QLabel("Center Freq (MHz)" + ": "))
        self._cf_line_edit = Qt.QLineEdit(str(self.cf))
        self._cf_tool_bar.addWidget(self._cf_line_edit)
        self._cf_line_edit.editingFinished.connect(
            lambda: self.set_cf(eng_notation.str_to_num(str(self._cf_line_edit.text()))))
        self.top_grid_layout.addWidget(self._cf_tool_bar, 0, 0, 1, 5)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 5):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._bw_tool_bar = Qt.QToolBar(self)
        self._bw_tool_bar.addWidget(Qt.QLabel("Bandwidth" + ": "))
        self._bw_line_edit = Qt.QLineEdit(str(self.bw))
        self._bw_tool_bar.addWidget(self._bw_line_edit)
        self._bw_line_edit.editingFinished.connect(
            lambda: self.set_bw(eng_notation.str_to_num(str(self._bw_line_edit.text()))))
        self.top_grid_layout.addWidget(self._bw_tool_bar, 0, 15, 1, 5)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(15, 20):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.rational_resampler_xxx_2 = filter.rational_resampler_fff(
                interpolation=48,
                decimation=80,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=10,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_0_1_0 = filter.rational_resampler_ccf(
                interpolation=48,
                decimation=800,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_0_1 = filter.rational_resampler_ccf(
                interpolation=48,
                decimation=800,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_0_0_0 = filter.rational_resampler_fff(
                interpolation=48,
                decimation=800,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_0_0_0.set_block_alias("rr")
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_fff(
                interpolation=48,
                decimation=800,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=10,
                taps=[],
                fractional_bw=0)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(False)

        self.qtgui_waterfall_sink_x_0.disable_legend()


        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.mt_grid_layout_0.addWidget(self._qtgui_waterfall_sink_x_0_win, 10, 0, 10, 10)
        for r in range(10, 20):
            self.mt_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 10):
            self.mt_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_1 = qtgui.time_sink_f(
            1024, #size
            48e3, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_1.set_update_time(0.10)
        self.qtgui_time_sink_x_0_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_1.enable_tags(True)
        self.qtgui_time_sink_x_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_1.enable_autoscale(False)
        self.qtgui_time_sink_x_0_1.enable_grid(False)
        self.qtgui_time_sink_x_0_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_1.enable_control_panel(False)
        self.qtgui_time_sink_x_0_1.enable_stem_plot(False)


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


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_1.qwidget(), Qt.QWidget)
        self.mt_grid_layout_3.addWidget(self._qtgui_time_sink_x_0_1_win, 1, 0, 20, 20)
        for r in range(1, 21):
            self.mt_grid_layout_3.setRowStretch(r, 1)
        for c in range(0, 20):
            self.mt_grid_layout_3.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
            8192, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            (cf*1e6), #fc
            (samp_rate/10), #bw
            "", #name
            1,
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

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.qwidget(), Qt.QWidget)
        self.mt_layout_2.addWidget(self._qtgui_freq_sink_x_0_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            (cf*1e6), #fc
            100e3, #bw
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
        self.qtgui_freq_sink_x_0.enable_axis_labels(False)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)

        self.qtgui_freq_sink_x_0.disable_legend()


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
        self.mt_grid_layout_0.addWidget(self._qtgui_freq_sink_x_0_win, 0, 0, 10, 10)
        for r in range(0, 10):
            self.mt_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 10):
            self.mt_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            5000, #size
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(False)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
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

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.qwidget(), Qt.QWidget)
        self.mt_layout_1.addWidget(self._qtgui_const_sink_x_0_win)
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq((cf*1e6), 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(gain, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
        self.filter_fft_low_pass_filter_0_0_1 = filter.fft_filter_ccc(10, firdes.low_pass(1, samp_rate, 100e3, 45e3, window.WIN_HAMMING, 6.76), 1)
        self.filter_fft_low_pass_filter_0_0_0 = filter.fft_filter_ccc(10, firdes.low_pass(1, samp_rate, 100e3, 10e3, window.WIN_HAMMING, 6.76), 1)
        self.filter_fft_low_pass_filter_0_0 = filter.fft_filter_ccc(10, firdes.low_pass(1, samp_rate, 100e3, 10e3, window.WIN_HAMMING, 6.76), 1)
        self.digital_costas_loop_cc_0_0 = digital.costas_loop_cc((6.28/100), 2, False)
        self.dc_blocker_xx_0 = filter.dc_blocker_ff(320, True)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_float*1,demodSelect,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_ff((10**(vol/20)))
        self.blocks_freqshift_cc_0_0 = blocks.rotator_cc(2.0*math.pi*67e3/((samp_rate/20)))
        self.blocks_freqshift_cc_0 = blocks.rotator_cc(2.0*math.pi*cfshift/48e3)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, 1)
        self.blocks_conjugate_cc_0 = blocks.conjugate_cc()
        self.blocks_complex_to_real_0_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_complex_to_arg_0 = blocks.complex_to_arg(1)
        self.audio_sink_1 = audio.sink(48000, '', True)
        self.analog_quadrature_demod_cf_0_0_0 = analog.quadrature_demod_cf(((samp_rate/10)/(2*math.pi*250e3)))
        self.analog_quadrature_demod_cf_0_0 = analog.quadrature_demod_cf(((samp_rate/10)/(2*math.pi*250e3)))
        self.analog_agc_xx_0_0 = analog.agc_cc((1e-4), 1.0, 1.0, 65536)
        self.analog_agc_xx_0 = analog.agc_cc((1e-4), 1.0, 1.0, 65536)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc_xx_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.analog_agc_xx_0_0, 0), (self.digital_costas_loop_cc_0_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0_0_0, 0), (self.rational_resampler_xxx_0_0_0, 0))
        self.connect((self.blocks_complex_to_arg_0, 0), (self.rational_resampler_xxx_2, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_selector_0, 1))
        self.connect((self.blocks_complex_to_real_0_0, 0), (self.blocks_selector_0, 2))
        self.connect((self.blocks_conjugate_cc_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_delay_0, 0), (self.blocks_conjugate_cc_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_freqshift_cc_0_0, 0))
        self.connect((self.blocks_freqshift_cc_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_freqshift_cc_0_0, 0), (self.filter_fft_low_pass_filter_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.audio_sink_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.qtgui_time_sink_x_0_1, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_complex_to_arg_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.dc_blocker_xx_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0, 0), (self.blocks_complex_to_real_0_0, 0))
        self.connect((self.filter_fft_low_pass_filter_0_0, 0), (self.analog_quadrature_demod_cf_0_0, 0))
        self.connect((self.filter_fft_low_pass_filter_0_0_0, 0), (self.analog_quadrature_demod_cf_0_0_0, 0))
        self.connect((self.filter_fft_low_pass_filter_0_0_1, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.filter_fft_low_pass_filter_0_0_1, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.filter_fft_low_pass_filter_0_0_1, 0), (self.filter_fft_low_pass_filter_0_0, 0))
        self.connect((self.filter_fft_low_pass_filter_0_0_1, 0), (self.qtgui_freq_sink_x_0, 1))
        self.connect((self.filter_fft_low_pass_filter_0_0_1, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.filter_fft_low_pass_filter_0_0_1, 0), (self.rational_resampler_xxx_0_1, 0))
        self.connect((self.filter_fft_low_pass_filter_0_0_1, 0), (self.rational_resampler_xxx_0_1_0, 0))
        self.connect((self.filter_fft_low_pass_filter_0_0_1, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.osmosdr_source_0, 0), (self.filter_fft_low_pass_filter_0_0_1, 0))
        self.connect((self.osmosdr_source_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.dc_blocker_xx_0, 0))
        self.connect((self.rational_resampler_xxx_0_0_0, 0), (self.blocks_selector_0, 4))
        self.connect((self.rational_resampler_xxx_0_1, 0), (self.blocks_freqshift_cc_0, 0))
        self.connect((self.rational_resampler_xxx_0_1_0, 0), (self.analog_agc_xx_0_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.blocks_delay_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.rational_resampler_xxx_2, 0), (self.blocks_selector_0, 3))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "signalAnalysis_1")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_vol(self):
        return self.vol

    def set_vol(self, vol):
        self.vol = vol
        self.blocks_multiply_const_vxx_0_0.set_k((10**(self.vol/20)))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_quadrature_demod_cf_0_0.set_gain(((self.samp_rate/10)/(2*math.pi*250e3)))
        self.analog_quadrature_demod_cf_0_0_0.set_gain(((self.samp_rate/10)/(2*math.pi*250e3)))
        self.blocks_freqshift_cc_0_0.set_phase_inc(2.0*math.pi*67e3/((self.samp_rate/20)))
        self.filter_fft_low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, 100e3, 10e3, window.WIN_HAMMING, 6.76))
        self.filter_fft_low_pass_filter_0_0_0.set_taps(firdes.low_pass(1, self.samp_rate, 100e3, 10e3, window.WIN_HAMMING, 6.76))
        self.filter_fft_low_pass_filter_0_0_1.set_taps(firdes.low_pass(1, self.samp_rate, 100e3, 45e3, window.WIN_HAMMING, 6.76))
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0_0.set_frequency_range((self.cf*1e6), (self.samp_rate/10))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.osmosdr_source_0.set_gain(self.gain, 0)

    def get_demodSelect(self):
        return self.demodSelect

    def set_demodSelect(self, demodSelect):
        self.demodSelect = demodSelect
        self._demodSelect_callback(self.demodSelect)
        self.blocks_selector_0.set_input_index(self.demodSelect)

    def get_cfshift(self):
        return self.cfshift

    def set_cfshift(self, cfshift):
        self.cfshift = cfshift
        self.blocks_freqshift_cc_0.set_phase_inc(2.0*math.pi*self.cfshift/48e3)

    def get_cf(self):
        return self.cf

    def set_cf(self, cf):
        self.cf = cf
        Qt.QMetaObject.invokeMethod(self._cf_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.cf)))
        self.osmosdr_source_0.set_center_freq((self.cf*1e6), 0)
        self.qtgui_freq_sink_x_0.set_frequency_range((self.cf*1e6), 100e3)
        self.qtgui_freq_sink_x_0_0.set_frequency_range((self.cf*1e6), (self.samp_rate/10))

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        Qt.QMetaObject.invokeMethod(self._bw_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.bw)))




def main(top_block_cls=signalAnalysis_1, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

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
