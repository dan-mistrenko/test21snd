import math
import numpy as np
import array as myarray


def an_ap_5(y0, dx, dy, lengtharr, signalout):
    for j in range(dx):
        if ((dx + j) < lengtharr):
            # signalout.append(y0)
            tmp = np.int16( ((np.cos(np.pi * (j / dx)) + 1.0) / 2.0) * dy + y0 )
            signalout.append(tmp.copy())

    return signalout


def exteremumslist(signal_in):
    exteremum0 = [[]]

    tmpini = [signal_in[0].copy(), 0, True, 1]
    exteremum0[0] = tmpini

    for i in range(len(signal_in) - 1):
        if (signal_in[i] > signal_in[i - 1]) and (signal_in[i] > signal_in[i + 1]):
            #  +
            # + +
            tmpmax = [signal_in[i].copy(), i, True, 0]
            exteremum0.append(tmpmax)

        if (signal_in[i] < signal_in[i - 1]) and (signal_in[i] < signal_in[i + 1]):
            # + +
            #  +
            tmpmin = [signal_in[i].copy(), i, False, 0]
            exteremum0.append(tmpmin)

        if (signal_in[i] > signal_in[i - 1]) and (signal_in[i] == signal_in[i + 1]):
            #  ++
            # +
            for k in range(i, len(signal_in) - 1):
                if signal_in[k] < signal_in[k + 1]:
                    break
                if signal_in[k] > signal_in[k + 1]:
                    weque = (i + k) // 2
                    tmpmaxshelf = [signal_in[weque].copy(), weque, True, 0]
                    exteremum0.append(tmpmaxshelf)
                    break

        if (signal_in[i] < signal_in[i - 1]) and (signal_in[i] == signal_in[i + 1]):
            # +
            #  ++
            for k in range(i, len(signal_in) - 1):
                if signal_in[k] > signal_in[k + 1]:
                    break
                if signal_in[k] < signal_in[k + 1]:
                    weque = (i + k) // 2
                    tmpminshelf = [signal_in[weque].copy(), weque, False, 0]
                    exteremum0.append(tmpminshelf)
                    break

    tmpdes = [signal_in[-1].copy(), len(signal_in), True, 1]

    exteremum0.append(tmpdes)

    return exteremum0


def handlings_test(signal_in):
    # exteremum0 = exteremumslist(signal_in)
    lengtharr = len(signal_in)
    # endvalue = signal_in[lengtharr - 1]

    wavewarr_0 = [0]
    for i in range(1, lengtharr): wavewarr_0.append(0)

    wavewarr_1 = [0]
    for i in range(1, lengtharr): wavewarr_1.append(0)

    return [wavewarr_0, wavewarr_1]


def handlings(signal_in):
    exteremum0 = exteremumslist(signal_in)
    lengtharr = len(signal_in)
    endvalue = signal_in[lengtharr - 1]

    wavewarr_1 = []
    wavewarr_0 = []

    y01 = 0
    y11 = 0
    dx1 = 0
    dy1 = 0
    i_1 = 0
    y00 = 0
    y10 = 0
    dx0 = 0
    dy0 = 0
    i_0 = 0

    for i in range(len(exteremum0)):
        if exteremum0[i][2]:
            dx1 = exteremum0[i][1] - y01
            # dy1 = exteremum0[i][0] - y11
            dy1 = exteremum0[i_1][0] - exteremum0[i][0]
            y01 = exteremum0[i][1]
            y11 = exteremum0[i][0]
            # print("i : " + str(i) + "; rep1 : " + str(rep1) + "; cnt1 : " + str(cnt1))
            wavewarr_1 = an_ap_5(exteremum0[i][0], dx1, dy1, lengtharr, wavewarr_1)
            i_1 = i

        else:
            dx0 = exteremum0[i][1] - y00
            # dy0 = exteremum0[i][0] - y10
            dy0 = exteremum0[i_0][0] - exteremum0[i][0]
            y00 = exteremum0[i][1]
            # y10 = exteremum0[i][0]
            # print("i : " + str(i) + "; rep0 : " + str(rep0) + "; cnt0 : " + str(cnt0))
            wavewarr_0 = an_ap_5(exteremum0[i][0], dx0, dy0, lengtharr, wavewarr_0)
            i_0 = i

    print("dowžyna wavewarr_1 :" + str(len(wavewarr_1)))
    print("dowžyna wavewarr_0 :" + str(len(wavewarr_0)))
    # wavewarr_1 = [np.int16(x) for x in wavewarr_1]
    # wavewarr_0 = [np.int16(x) for x in wavewarr_0]
    return [wavewarr_0, wavewarr_1]


def aprox(signal_in):
    exteremum0 = exteremumslist(signal_in)
    lengtharr = len(signal_in)
    endvalue = signal_in[lengtharr - 1]

    wavewarr = []

    y01 = 0
    y11 = 0
    dx1 = 0
    dy1 = 0
    i_1 = 0

    for i in range(len(exteremum0)):
        dx1 = exteremum0[i][1] - y01
        # dy1 = exteremum0[i][0] - y11
        dy1 = exteremum0[i_1][0] - exteremum0[i][0]
        y01 = exteremum0[i][1]
        y11 = exteremum0[i][0]
        # print("i : " + str(i) + "; rep1 : " + str(rep1) + "; cnt1 : " + str(cnt1))
        wavewarr = an_ap_5(exteremum0[i][0], dx1, dy1, lengtharr, wavewarr)
        i_1 = i

    print("dowžyna wavewarr :" + str(len(wavewarr)))
    return wavewarr


def handlings_S(signal_in):
    exteremum0 = exteremumslist(signal_in)
    lengtharr = len(signal_in)
    endvalue = signal_in[lengtharr - 1]


    wavewarr_1 = list()
    wavewarr_0 = list()

    x01 = 0
    y01 = 0
    dx1 = 0
    dy1 = 0
    i_1 = 0
    x00 = 0
    y00 = 0
    dx0 = 0
    dy0 = 0
    i_0 = 0

    for i in range(-1, len(exteremum0) - 1):
        if exteremum0[i][2]:
            dx1 = exteremum0[i][1] - x01
            # dx1 = exteremum0[i][1] - exteremum0[i_1][1]
            dy1 = exteremum0[i][0] - y01
            # dy1 = exteremum0[i_1][0] - exteremum0[i][0]
            x01 = exteremum0[i][1]
            y01 = exteremum0[i][0]
            # print("i : " + str(i) + "; rep1 : " + str(rep1) + "; cnt1 : " + str(cnt1))
            wavewarr_1 = an_ap_5(exteremum0[i_1][0], dx1, dy1, lengtharr, wavewarr_1)
            i_1 = i
        else:
            dx0 = exteremum0[i][1] - x00
            # dx0 = exteremum0[i][1] - exteremum0[i_0][1]
            dy0 = exteremum0[i][0] - y00
            # dy0 = exteremum0[i_0][0] - exteremum0[i][0]
            x00 = exteremum0[i][1]
            y00 = exteremum0[i][0]
            # print("i : " + str(i) + "; rep0 : " + str(rep0) + "; cnt0 : " + str(cnt0))
            wavewarr_0 = an_ap_5(exteremum0[i_0][0], dx0, dy0, lengtharr, wavewarr_0)
            i_0 = i

    print("dowžyna wavewarr_1 :" + str(len(wavewarr_1)))
    print("dowžyna wavewarr_0 :" + str(len(wavewarr_0)))
    return [wavewarr_0, wavewarr_1]
