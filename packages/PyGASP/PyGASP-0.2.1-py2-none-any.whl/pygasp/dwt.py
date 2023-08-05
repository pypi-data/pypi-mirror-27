import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.figure import Figure
import matplotlib.gridspec as gridspec
import copy
import itertools


# ----------------------Begin forward transform functions----------------------

def _chooseWavelet(wav):
    if wav == 'haar':
        h = (1.0/math.sqrt(2), 1.0/math.sqrt(2))
        g = (1.0/math.sqrt(2), -1.0/math.sqrt(2))
    elif wav == 'db2':
        bot = 4*2**.5
        h = [(1.0+3**.5)/bot, (3.0 + 3**.5)/bot, (3.0-3**.5)/bot,
             (1.0-3**.5)/bot]
        g = [(1.0-3**.5)/bot, -1*(3.0-3**.5)/bot, (3.0 + 3**.5)/bot,
             -1*(1.0+3**.5)/bot]
    elif wav == 'db3':
        outer = (2**.5)/32
        inner = (5 + 2*10**.5)**.5
        h = [outer*(1 + 10**.5 + inner),
             outer*(5 + 10**.5 + 3*inner),
             outer*(10 - 2*10**.5 + 2*inner),
             outer*(10 - 2*10**.5 - 2*inner),
             outer*(5 + 10**.5 - 3*inner),
             outer*(1 + 10**.5 - inner)]
        g = []
        for i in range(len(h)):
            g.append(((-1)**i)*h[5-i])
    elif wav == 'db4':
        h = [0.23037781330885523, 0.71484657055254153,
             0.63088076792959036, -0.027983769416983849,
             -0.18703481171888114, 0.030841381835986965,
             0.032883011666982945, -0.010597401784997278]
        g = [-0.010597401784997278, -0.032883011666982945,
             0.030841381835986965, 0.18703481171888114,
             -0.027983769416983849, -0.63088076792959036,
             0.71484657055254153, -0.23037781330885523]
    elif wav == 'coif1':
        h = [-.0156557281, .07273226195, .3848648469,
             -.8525720202, .3378976625, .0727326195]
        g = [-.0727326195, .3378976625, .8525720202,
             .3848648469, -.0727326195, -.0156557281]  # CHECK FOR CORRECTNESS!
    else:
        print 'Wavelet \'%s\' not found.  Using haar.' % (wav)
        return _chooseWavelet('haar')

    '''elif wav == 'db3':
        h = [0.3326705530, 0.8068915093, 0.4598775021, -0.1350110200,
             -0.0854412739, 0.0352262919]
        g = [0.0352262919, 0.0854412739, -0.1350110200, -0.4598775021,
             0.8068915093, -0.3326705530]'''

    return h, g


def dwt(signal, wav='haar', levels=-1, mode='zpd'):
    """Performs a dwt on a given signal.

    This function performs a dwt on signal using CUDA GPU.

    :param signal: signal
    :param wav: Wavelet to use while performing dwt.
        Full list of available wavelets can be found ...
    :param levels: Number of levels of dwt to perform.
        If levels=-1, full decomposition is done, equivalent to
        levels = floor(log(len(signal), 2))
    :param mode: Padding mode to use to deal with boundary conditions.
        Full list of available padding modes can be found ...
    :type signal: list, numpy array
    :type wav: string
    :type levels: int
    :type mode: string
    :returns: transformed signal
    :rtype: list of arrays
    """

    if levels == -1:
        levels = math.floor(math.log(len(signal), 2))
    elif levels < -1:
        return -1
    h, g = _chooseWavelet(wav)

    return _dwt_rec(signal, h, g, wav, levels, mode)


def dwt2(image, wav='haar', mode='zpd'):
    """Performs a 2-dimensional dwt on an image.

    This function performs a 2-dimensional dwt on an image using CUDA GPU.

    :param image: image
    :param wav: Wavelet to use while performing 2-dimensional dwt.
        Full list of available wavelets can be found ...
    :param mode: Padding mode to use to deal with boundary conditions.
        Full list of available padding modes can be found ...
    :type image: list of lists, 2-d numpy array
    :type wav: string
    :type mode: string
    :returns: transformed image
    :rtype: 2-tuple containing (cA, (cH, cV, cD))
    """

    ONE_LEVEL = 1
    h, g = _chooseWavelet(wav)
    temp = np.array(image)

    transLow = []
    transHigh = []
    m = len(temp)
    for i in range(m):
        trans = _dwt_rec(temp[i], h, g, wav, ONE_LEVEL, mode)
        transLow.append(trans[0])
        transHigh.append(trans[1])

    transLow = np.array(transLow)
    transHigh = np.array(transHigh)

    transLowL = []
    transLowH = []
    m = len(transLow[0])
    for i in range(m):
        trans = _dwt_rec(transLow[:, i], h, g, wav, ONE_LEVEL, mode)
        transLowL.append(trans[0])
        transLowH.append(trans[1])

    transHighL = []
    transHighH = []
    m = len(transHigh[0])
    for i in range(m):
        trans = _dwt_rec(transHigh[:, i], h, g, wav, ONE_LEVEL, mode)
        transHighL.append(trans[0])
        transHighH.append(trans[1])

    transLowL = np.transpose(transLowL)
    transLowH = np.transpose(transLowH)
    transHighL = np.transpose(transHighL)
    transHighH = np.transpose(transHighH)

    transformed = (transLowL, (transLowH, transHighL, transHighH))

    return transformed


def _extend(signal, length, mode='zpd'):
    pad = length-2
    if mode == 'zpd':
        for i in range(pad):
            signal = np.concatenate(([0], signal, [0]))
        if len(signal) % 2 != 0:
            signal = np.concatenate((signal, [0]))
    elif mode == 'ppd':
        for i in range(pad):
            signal = np.concatenate(([signal[-(1+2*i)]],
                                     signal,
                                     [signal[2*i]]))
        if len(signal) % 2 != 0:
            signal = np.concatenate((signal, [signal[2*pad]]))
    else:
        print 'Padding not understood. Returning zero-padding.'
        return _extend(signal, length, 'zpd')

    return signal


def _dwt_rec(signal, h, g, wav, levels, mode):
    N = len(signal)
    F = len(h)

    if levels == 0:
        return [np.array(signal)]

    signal = _extend(signal, F, mode)
    size = (N+1)/2+(F-2)/2

    yHigh = np.zeros(size)
    yLow = np.zeros(size)

    for k in range(size):
        sumH = 0
        sumG = 0
        for n in range(len(h)):
            element = signal[2*k + n]
            sumH += element*h[n]
            sumG += element*g[n]
        yHigh[k] = sumG
        yLow[k] = sumH

    coefs = _dwt_rec(yLow, h, g, wav, levels-1, mode)
    coefs.append(np.array(yHigh))

    return coefs


# ----------------------Begin inverse transform functions----------------------

def _chooseInverseWavelet(wav):
    if wav == 'haar':
        h = (1.0/math.sqrt(2), 1.0/math.sqrt(2))
        g = (-1.0/math.sqrt(2), 1.0/math.sqrt(2))
    elif wav == 'db2':
        h = [-0.1294095226, 0.224143868, 0.8365163037, 0.4829629131]
        g = [-0.4829629131, 0.8365163037, -0.224143868, -0.1294095226]
    elif wav == 'db3':
        h = [0.0352262919, -0.0854412739, -0.13501102, 0.4598775021,
             0.8068915093, 0.332670553]
        g = [-0.332670553, 0.8068915093, -0.4598775021, -0.13501102,
             0.0854412739, 0.0352262919]
    elif wav == 'db4':
        h = [-0.0105974018, 0.0328830117, 0.0308413818, -0.1870348117,
             -0.0279837694, 0.6308807679, 0.7148465706, 0.2303778133]
        g = [-0.2303778133, 0.7148465706, -0.6308807679, -0.0279837694,
             0.1870348117, 0.0308413818, -0.0328830117, -0.0105974018]
    else:
        print 'Wavelet \'%s\' not found.  Using haar.' % (wav)
        return _chooseInverseWavelet('haar')

    return h, g


def idwt(transformed, wav='haar', levels=-1, mode='zpd'):
    """Performs an inverse dwt on a given transformed signal.

    This function performs an inverse dwt on a transformed signal using CUDA
    GPU.

    :param transformed: transformed signal
    :param wav: Wavelet to use while performing inverse dwt.
        Full list of available wavelets can be found ...
    :param levels: Number of levels of inverse dwt to perform.
        If levels=-1, full decomposition is done, equivalent to
        levels = floor(log(len(signal), 2))
    :param mode: Padding mode to use to deal with boundary conditions.
        Full list of available padding modes can be found ...
    :type transformed: list, numpy array
    :type wav: string
    :type levels: int
    :type mode: string
    :returns: inverted signal
    :rtype: numpy array
    """

    if levels < -1:
        return -1
    h, g = _chooseInverseWavelet(wav)
    return _inverse_rec(copy.copy(transformed), h, g, levels, mode)


def idwt2(transformed, wav='haar', mode='zpd'):
    """Performs a 2-dimensional inverse dwt on a transformed image.

    This function performs a 2-dimensional inverse dwt on a transformed image
    using CUDA GPU.

    :param transformed: transformed image
    :param wav: Wavelet to use while performing inverse 2-dimensional dwt.
        Full list of available wavelets can be found ...
    :param mode: Padding mode to use to deal with boundary conditions.
        Full list of available padding modes can be found ...
    :type transformed: list of lists, 2-d numpy array
    :type wav: string
    :type mode: string
    :returns: inverted image
    :rtype: 2-d numpy array
    """

    ONE_LEVEL = 1
    h, g = _chooseInverseWavelet(wav)

    temp = copy.copy(transformed)
    cA = temp[0]
    cH = temp[1][0]
    cV = temp[1][1]
    cD = temp[1][2]

    transLowL = np.transpose(cA)
    transLowH = np.transpose(cH)
    transHighL = np.transpose(cV)
    transHighH = np.transpose(cD)

    left = []  # transLow
    right = []  # transHigh

    for i in range(len(cA)):
        left.append(idwt([transLowL[:, i], transHighL[:, i]], wav, ONE_LEVEL,
                         mode))
        right.append(idwt([transLowH[:, i], transHighH[:, i]], wav, ONE_LEVEL,
                          mode))
    left = np.transpose(np.array(left))
    right = np.transpose(np.array(right))

    image = []
    for i in range(len(left)):
        image.append(idwt([left[i], right[i]], wav, ONE_LEVEL, mode))

    return np.transpose(np.array(image))


def _extendInverse(signal, length, mode='zpd'):
    pad = length - 1
    if mode == 'zpd':
        for i in range(pad):
            signal = np.concatenate((signal, [0]))
    elif mode == 'ppd':
        for i in range(pad):
            signal = np.concatenate((signal, [signal[i]]))
    else:
        print 'Padding not understood. Returning zero-padding.'
        return _extendInverse(signal, length, 'zpd')

    return signal, pad


# Changed to use levels without testing for correctness (11/6/12)
def _inverse_rec(transformed, h, g, levels, mode):
    N = len(transformed)

    if levels == 0:
        return transformed[0]

    if N == 1:
        return transformed[0]

    F = len(h)
    startLen = len(transformed[1])
    newAvgs = []

    low = transformed[0]
    low, pad = _extendInverse(low, F, mode)
    high = transformed[1]
    high, pad = _extendInverse(high, F, mode)

    for i in range(startLen):
        even = odd = 0
        for j in range(F/2):
            odd += h[1+2*j]*low[i+j] + g[1+2*j]*high[i+j]
            even += h[2*j]*low[i+j] + g[2*j]*high[i+j]
        newAvgs.append(odd)
        newAvgs.append(even)
    transformed.pop(0)
    transformed.pop(0)
    if 1-pad != 0:
        transformed.insert(0, np.array(newAvgs)[:-pad+1])
    else:
        transformed.insert(0, np.array(newAvgs))

    return _inverse_rec(transformed, h, g, levels-1, mode)


# ------Begin other functions------

# the x axis is not marked correctly (2/4/2013)
# should the colors be percentages? right now they are just scaled coefficients
# for ideas, http://support.sas.com/rnd/app/da/new/802ce/iml/chap1/sect8.htm
def scalogram(coefs, do_scaling=1, scale_power=.3, log_y_axis=1, create_bar=1):
    """Creates and displays a scalogram from a set of wavelet-transformed
    coefficients.

    :param coefs: wavelet-transformed 1-D signal
    :param do_scaling: Determines whether detail coefficients are magnified to
        increase the emphasis placed on them.
    :param scale_power: If do_scaling is on, this controls how much emphasis is
        placed on the detail coefficients. Smaller values mean more emphasis.
    :param log_y_axis: If set to 1, this causes the levels to be evenly spaced
        along the vertical axis.  This distorts frequency interpretation.
    :param create_bar: When set, this creates a vertical bar next to the graph
        the displays the relative power of each level of coefficients.
    :type coefs: list of numpy arrays
    :type do_scaling: boolean
    :type scale_power: floating-point value between (0, 1) exclusive
    :type log_y_axis: boolean
    :type create_bar: boolean
    """

    DO_SCALING = do_scaling
    SCALE_POWER = scale_power
    LOG_Y_AXIS = log_y_axis
    CREATE_BAR = create_bar

    if not DO_SCALING:
        biggest = max(map(lambda x: max(x**2), coefs))*1.0
        smallest = min(map(lambda x: min(x**2), coefs))
        diff = biggest - smallest
    else:
        biggest = 0
        smallest = 0
        diff = 1

    if LOG_Y_AXIS:
        heights = range(len(coefs)+1)
        height = len(coefs)
    else:
        heights = [0]
        height = 0
        for i in range(len(coefs)):
            height += 2**i
            heights.append(height)

    colorPowers = []
    if CREATE_BAR:
        sumSquared = []
        totSquared = 0.0
        for i in range(len(coefs)):
            thisSum = sum(map(lambda x: x**2, coefs[i]))
            sumSquared.append(thisSum)
            totSquared += thisSum
        percentPowers = [sumSquared[i] / totSquared for i in range(len(coefs))]
        bigPower = max(percentPowers)
        smallPower = min(percentPowers)
        diffPower = bigPower-smallPower
        colorPowers = [(percentPowers[i] - smallPower)/diffPower
                       for i in range(len(coefs))]

        barWidth = .1

        gs = gridspec.GridSpec(1, 2, width_ratios=[1, 10])
        ax2 = plt.subplot(gs[0])
        ax2.set_xlim(0, barWidth)
        ax2.set_ylim(0, height)
        ax2.get_xaxis().set_ticks([])
        ax2.get_yaxis().set_ticks(
            [heights[i] + (heights[i+1]-heights[i]) / 2.0
             for i in range(len(heights)-1)])
        ax2.get_yaxis().set_ticklabels(range(len(coefs)))
        ax = plt.subplot(gs[1])
        ax.get_yaxis().set_ticks([])
    else:
        ax = plt.subplot(111)
        ax.get_yaxis().set_ticks(
            [heights[i] + (heights[i+1]-heights[i]) / 2.0
             for i in range(len(heights)-1)])
        ax.get_yaxis().set_ticklabels(range(len(coefs)))

    ax.get_xaxis().set_ticks([])

    width = 1
    ax.set_ylim(0, height)
    ax.set_xlim(0, width)

    for level in range(len(coefs)):
        time = 0
        xstep = float(width) / len(coefs[level])
        ystep = heights[level+1]-heights[level]
        if DO_SCALING:
            biggest = max(coefs[level]**2) * 1.0
            smallest = min(coefs[level]**2)
            diff = biggest - smallest

        for time in range(len(coefs[level])):
            color = ((coefs[level][time])**2 - smallest) / diff
            if DO_SCALING:
                color = color**SCALE_POWER
            ax.add_patch(Rectangle(
                (time*xstep, heights[level]),
                xstep,
                ystep,
                color=(color, 0, .5)))

        if CREATE_BAR:
            ax2.add_patch(Rectangle(
                (0, heights[level]),
                barWidth,
                ystep,
                color=(colorPowers[level], 0, .5)
                ))
            ax2.plot([0, barWidth], [heights[level+1], heights[level+1]],
                     "w-", linewidth=2)

    plt.tight_layout()
    plt.show()


# what to do with axis labels? (2/4/13)
# are these in the correct order (first & last)? (2/4/13)
def plot(coefs, quiet=False, fig=None):
    """Plots each level of wavelet coefficients on its own set of axes.

    :param coefs: wavelet-transformed 1-D signal
    :type coefs: list of numpy arrays
    """

    numPlots = len(coefs)
    axes = []
    if fig is None:
        fig = Figure()
    for i in range(numPlots):
        p = fig.add_subplot(numPlots, 1, i)
        axes.append(p)
        p.get_xaxis().set_ticks([])
        p.get_yaxis().set_ticks([])
        title = "Detail Coefficients at Level %d" % (numPlots-i)
        if i == 0:
            title = "Average Coefficients"
        p.set_title(title)
        p.plot(coefs[i])

    plt.tight_layout()
    if not quiet:
        plt.show()
    else:
        return fig
