import numpy as np
from scipy import signal

def lowpass_butter(sig, fs, cutoff, order=4, block_size=64):
    return butter("lowpass", sig, fs, cutoff, order=order, block_size=block_size)

def highpass_butter(sig, fs, cutoff, order=4, block_size=64):
    return butter("highpass", sig, fs, cutoff, order=order, block_size=block_size)

def bandpass_butter(sig, fs, cutoff, order=4, block_size=64):
    return butter("bandpass", sig, fs, cutoff, order=order, block_size=block_size)

# General function for butterworth filters of different types
def butter(btype, sig, fs, cutoff, order=4, block_size=64):
    # Now supports varying cutoff
    # Credit goes to ChatGPT
    output = np.zeros_like(sig, dtype=float)
    zi = None

    for i in range(0, len(sig), block_size):
        end = min(i + block_size, len(sig))
        current_cutoff = np.mean(cutoff[i:end], axis=0)
        sos = signal.butter(order, current_cutoff, btype=btype, fs=fs, output='sos')
        if zi is None:
            zi = np.zeros((sos.shape[0], 2))

        output[i:end], zi = signal.sosfilt(sos, sig[i:end], zi=zi)

    return output, sos

def allpass(sig, a):
    b = [a, 1]
    den = [1, a]
    sos = signal.tf2sos(b, den)
    return signal.sosfilt(sos, sig), sos
