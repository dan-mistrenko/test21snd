import sys
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from itertools import zip_longest
import numpy as np
import random
import wave, struct, pygame # pyaudio, math
# from scipy.interpolate import interp1d
import time
from mykernel import aprox, handlings, exteremumslist


class MatplotlibWidget(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        loadUi("qt_window.ui", self)

        self.signal = []
        self.signal_length = 0

        self.plotseries = []
        self.checkedSeries = []
        self.SeriesCount = 0
        self.soundItem = -1
        self.exteremums = []

        self.setWindowTitle("PyQt5 & Matplotlib Example GUI")
        # self.toolBar.addAction(exitAction)

        self.vbox = QVBoxLayout()
        self.grb_Series.setLayout(self.vbox)

        # self.btn_setarr.clicked.connect(self.serieconnect)
        self.btn_AddSerie.clicked.connect(self.addserie)

        self.cmb_Sound.currentTextChanged.connect(self.changesound)

        self.act_Open.triggered.connect(self.openwave16)
        self.act_Save.triggered.connect(self.savewave16)
        self.act_Close.triggered.connect(self.closeapp)

        # self.act_Plot.triggered.connect(self.update_graph)
        self.act_Plot.triggered.connect(self.upplot)
        self.act_Table.triggered.connect(self.uptable)
        self.act_Sound.triggered.connect(self.upsound)
        self.act_Add_Serie.triggered.connect(self.addserie)
        self.act_Addgrid.triggered.connect(self.addgrid)

        self.act_Filtering.triggered.connect(self.filtering)
        self.act_Filtering_16.triggered.connect(self.filtering_16)
        self.act_Minmax.triggered.connect(self.minmax)
        self.act_Truba.triggered.connect(self.truba)
        self.act_Aproximate.triggered.connect(self.aproximate)

        self.act_Add_arrays.triggered.connect(self.add_arrays)
        self.act_Mult_const.triggered.connect(self.mult_const)

        # self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self.tab_1))
        self.nav = NavigationToolbar(self.MplWidget.canvas, self.tab_1, coordinates=False)
        self.nav.setMinimumWidth(300)
        self.nav.setStyleSheet("QToolBar { border: 0px }")


    #### ######## Obrobka knopok ###############


    def openwave16(self):
        dialog = QFileDialog(self)
        dialog.setWindowTitle('Open WAV File')
        dialog.setNameFilter('WAV files (*.wav)')
        dialog.setFileMode(QFileDialog.ExistingFile)
        if dialog.exec_() == QDialog.Accepted:
            filename = str(dialog.selectedFiles()[0])
            spf = wave.open(filename, "r")

            # Extract Raw Audio from Wav File
            self.signal = spf.readframes(-1)
            self.signal = np.fromstring(self.signal, "Int16")
            self.signal_length = len(self.signal)
            print("file "+filename+" blahopolučno vidkryto")
            print("dovžyna zvukovoho masyvu : "+str(self.signal_length))

            self.addserie()

            # If Stereo
            if spf.getnchannels() == 2:
                print("Just mono files")
                sys.exit(0)
        else:
            return None

        return


    def savewave16(self):
        # dialog = QFileDialog(self)
        filename = QFileDialog.getSaveFileName(self, 'Save File')[0]
        if filename != '':
            print(str(filename))
            wav_file = wave.open(filename, "w")

            # wav params
            nchannels = 1
            sampwidth = 2
            sample_rate = 44100.0
            nframes = len(self.signal) // 2
            comptype = "NONE"
            compname = "not compressed"
            wav_file.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))
            # WAV files here are using short, 16 bit, signed integers for the
            # sample size.  So we multiply the floating point data we have by 32767, the
            # maximum value for a short integer.  NOTE: It is theortically possible to
            # use the floating point -1.0 to 1.0 data directly in a WAV file but not
            # obvious how to do that using the wave module in python.
            for sample in self.signal:
                wav_file.writeframes(struct.pack('h', sample))

            wav_file.close()
            print("file "+filename+" blahopolučno zbereženo")
        else:
            return None

        return


    def closeapp(self):
        self.close()


    def update_graph(self):
        fs = 500
        f = random.randint(1, 100)
        ts = 1 / fs
        self.length_of_signal = len(self.signal)
        # 100
        t = np.linspace(1, self.length_of_signal, self.length_of_signal)

        # cosinus_signal = np.cos(2 * np.pi * f * t)
        # sinus_signal = np.sin(2 * np.pi * f * t)

        self.tableWidget.setRowCount(self.length_of_signal)
        # self.tableWidget.setColumnCount(2)
        # self.tableWidget.horizontalHeaderItem(1).setTextAlignment(Qt.AlignLeft)
        # self.tableWidget.horizontalHeaderItem(2).setTextAlignment(Qt.AlignLeft)

        for k in range(0, self.length_of_signal):
            self.tableWidget.setItem(k, 0, QTableWidgetItem(str(self.plotseries[0][k])))
            # self.tableWidget.setItem(k, 0, QTableWidgetItem(str(self.signal[k])))
            # self.tableWidget.setItem(k, 0, QTableWidgetItem(str(cosinus_signal[k])))
            # self.tableWidget.setItem(k, 1, QTableWidgetItem(str(sinus_signal[k])))

        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(t, self.plotseries[0])
        # self.MplWidget.canvas.axes.plot(t, self.signal)
        # self.MplWidget.canvas.axes.plot.scatter(x,y)
        # self.MplWidget.canvas.axes.plot(t, cosinus_signal)
        # self.MplWidget.canvas.axes.plot(t, sinus_signal)
        # self.MplWidget.canvas.axes.legend(('cosinus', 'sinus'), loc='upper right')
        self.MplWidget.canvas.axes.grid()
        self.MplWidget.canvas.axes.set_title('Wave Signal')
        self.MplWidget.canvas.draw()


    def upplot(self):
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.draw()
        for next in range(len(self.plotseries)):

            if self.checkedSeries[next]:
                self.length_of_signal = len(self.plotseries[next])   # len(self.signal)
                t = np.linspace(0, self.length_of_signal, self.length_of_signal)
                self.tableWidget.setRowCount(self.length_of_signal)

                for k in range(0, self.length_of_signal):
                # for k in range(0, len(self.plotseries[next])):
                    self.tableWidget.setItem(k, 0, QTableWidgetItem(str(self.plotseries[next][k])))

                # self.MplWidget.canvas.axes.clear()
                self.MplWidget.canvas.axes.plot(t, self.plotseries[next])
                # self.MplWidget.canvas.axes.plot.scatter(x,y)

            # self.MplWidget.canvas.axes.grid()
            # self.MplWidget.canvas.axes.plot(t, cosinus_signal)
            # self.MplWidget.canvas.axes.plot(t, sinus_signal)
            # self.MplWidget.canvas.axes.legend(('cosinus', 'sinus'), loc='upper right')
            self.MplWidget.canvas.axes.set_title('Wave Signal')
            self.MplWidget.canvas.draw()


    def uptable(self):
        tmp_length_of_signal = 0

        for next in range(len(self.plotseries)):
            if self.checkedSeries[next]:
                if tmp_length_of_signal < len(self.plotseries[next]):
                    tmp_length_of_signal = len(self.plotseries[next])  # len(self.signal)

        for next in range(len(self.plotseries)):

            if self.checkedSeries[next]:
                self.tableWidget.setRowCount(tmp_length_of_signal)

                # for k in range(0, self.length_of_signal):
                for k in range(0, len(self.plotseries[next])):
                    self.tableWidget.setItem(k, next, QTableWidgetItem(str(self.plotseries[next][k])))


    def upsound(self):
        pygame.mixer.init(44100, -16, 1, 1024)
        # tmpbuffer = self.plotseries[self.soundItem].copy()
        tmpbuffer = (self.plotseries[self.soundItem]
                   * np.arange(1, len(self.plotseries[self.soundItem]) + 1, 1) //
                   np.arange(1, len(self.plotseries[self.soundItem]) + 1, 1)).astype(np.int16)

        sound = pygame.mixer.Sound(buffer=tmpbuffer)
        sound.play()


    def addserie(self):
        self.SeriesCount+=1

        newradiobutton = QCheckBox("Serie_"+str(self.SeriesCount), self)
        newradiobutton.setChecked(False)
        newradiobutton.setObjectName("rdb_Serie_"+str(self.SeriesCount))
        newradiobutton.clicked.connect(self.changeplot)
        self.vbox.addWidget(newradiobutton) # addButton(newradiobutton)
        self.grb_Radio.setLayout(self.vbox)
        name = newradiobutton.objectName()
        print(name)

        tmpsignal = self.signal.copy()
        self.plotseries.append(tmpsignal)
        self.checkedSeries.append(False)

        self.cmb_Sound.addItem("Serie_"+str(self.SeriesCount))
        self.cmb_Serie_in1.addItem("Serie_"+str(self.SeriesCount))
        self.cmb_Serie_in2.addItem("Serie_"+str(self.SeriesCount))
        self.cmb_Serie_out.addItem("Serie_"+str(self.SeriesCount))


    def addgrid(self):
        self.MplWidget.canvas.axes.grid()
        # self.MplWidget.canvas.axes.set_title('Wave Signal')
        self.MplWidget.canvas.draw()


    def changeplot(self):
        sender = self.sender()
        sender.setChecked(sender.isChecked())
        tmpname = sender.objectName()
        self.checkedSeries[int(tmpname[10:])-1] = sender.isChecked()
        print(self.checkedSeries[int(tmpname[10:])-1])


    def changesound(self):
        textItem = self.cmb_Sound.currentText()
        self.soundItem = int(textItem[6:]) - 1
        print(str(self.soundItem))


    def filtering(self):
        In_Item = int(self.cmb_Serie_in1.currentText()[6:]) - 1
        OutItem = int(self.cmb_Serie_out.currentText()[6:]) - 1
        fltbase = int(self.led_begin.text())
        acseler = int(self.led_count.text())
        hlfbase = fltbase // 2
        # print("Vchid : " + str(In_Item) + " , vychid : " + str(OutItem))
        for i in range(0, hlfbase):
            self.plotseries[OutItem][i] = self.plotseries[In_Item][hlfbase]
        for j in range(0, hlfbase):
            self.plotseries[OutItem][self.length_of_signal - 1 - hlfbase + j] = self.plotseries[In_Item][self.length_of_signal - 1]
        for k in range(0, self.length_of_signal - fltbase):
            tmpsample = 0
            for l in range(0, fltbase):
                tmpsample += self.plotseries[In_Item][k + l]
            self.plotseries[OutItem][k + hlfbase] = np.int16(acseler*tmpsample / fltbase)


    def filtering_16(self):
        In_Item = int(self.cmb_Serie_in1.currentText()[6:]) - 1
        OutItem = int(self.cmb_Serie_out.currentText()[6:]) - 1
        # print("Vchid : " + str(In_Item) + " , vychid : " + str(OutItem))
        for i in range(0, 8):
            self.plotseries[OutItem][i] = self.plotseries[In_Item][8]
        for j in range(0, 8):
            self.plotseries[OutItem][self.length_of_signal - 9 + j] = self.plotseries[In_Item][self.length_of_signal - 1]
        for k in range(0, self.length_of_signal - 16):
            tmpsample = 0
            for l in range(0, 16):
                tmpsample += self.plotseries[In_Item][k + l]
            self.plotseries[OutItem][k + 8] = np.int16(tmpsample / 16)


    def truba(self):
        start_time = time.time()

        In_Item = int(self.cmb_Serie_in1.currentText()[6:]) - 1
        OutItem = int(self.cmb_Serie_out.currentText()[6:]) - 1
        self.plotseries[OutItem], self.plotseries[OutItem + 1] = handlings(self.plotseries[In_Item])

        print("--- %s seconds ---" % (time.time() - start_time))


    def aproximate(self):
        start_time = time.time()

        In_Item = int(self.cmb_Serie_in1.currentText()[6:]) - 1
        OutItem = int(self.cmb_Serie_out.currentText()[6:]) - 1
        self.plotseries[OutItem] = aprox(self.plotseries[In_Item])

        print("--- %s seconds ---" % (time.time() - start_time))


    def minmax(self):
        start_time = time.time()

        In_Item = int(self.cmb_Serie_in1.currentText()[6:]) - 1
        # OutItem = int(self.cmb_Serie_out.currentText()[6:]) - 1

        self.exteremums = exteremumslist(signal_in=self.plotseries[In_Item])
        self.tableWidget.setRowCount(len(self.exteremums))
        self.tableWidget.setColumnCount(4)
        print("RowCount : " + str(len(self.exteremums[In_Item])) + " str(len(self.exteremums)) : " + str(len(self.exteremums)))
        for k in range(0, len(self.exteremums)):
            self.tableWidget.setItem(k, 1, QTableWidgetItem(str(self.exteremums[k])))
            # self.tableWidget.setItem(k, 1, QTableWidgetItem(str(self.exteremums[k][0])))
            # self.tableWidget.setItem(k, 2, QTableWidgetItem(str(self.exteremums[k][1])))
            # self.tableWidget.setItem(k, 3, QTableWidgetItem(str(self.exteremums[k][2])))

        print("--- %s seconds ---" % (time.time() - start_time))


    def add_arrays(self):
        start_time = time.time()

        InItem1 = int(self.cmb_Serie_in1.currentText()[6:]) - 1
        InItem2 = int(self.cmb_Serie_in2.currentText()[6:]) - 1
        OutItem = int(self.cmb_Serie_out.currentText()[6:]) - 1
        # const = int(self.led_begin.text())
        self.plotseries[OutItem] = [(a + b * int(self.led_begin.text())) for a, b in
                                    zip_longest(self.plotseries[InItem1], self.plotseries[InItem2], fillvalue=0)]
            # zip_longest(self.plotseries[InItem1],self.plotseries[InItem2], fillvalue=0)

        print("--- %s seconds ---" % (time.time() - start_time))


    def mult_const(self):
        start_time = time.time()

        In_Item = int(self.cmb_Serie_in1.currentText()[6:]) - 1
        OutItem = int(self.cmb_Serie_out.currentText()[6:]) - 1
        self.plotseries[OutItem] = [np.int16(a * float(self.led_begin.text())) for a, b in
                                    zip_longest(self.plotseries[In_Item], self.plotseries[0], fillvalue=0)]
        # print("--- qwe ---" + self.led_begin.text())
        print("--- %s seconds ---" % (time.time() - start_time))


def main():
    app = QApplication([])
    window = MatplotlibWidget()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
