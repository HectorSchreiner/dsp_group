import numpy as np

# Get magnitudes and frequencies from the spectrum of a signal
def make_spectrum_r(signal, fs):
    N = len(signal)
    Y = np.fft.rfft(signal) / N
    freq = np.fft.rfftfreq(N, d=1/fs)
    Y[1:-1] *= 2
    return Y, freq


# Convert a magnitude to decbel
def get_decibel(mag):
    return 20*np.log10(mag)


# Get the time vector from sampling frequency and time
def get_time_vector(fs, T_s):
    # Get total amount of samples
    N = int(round(fs * T_s))
    n = np.arange(N)
    # Divide by sampling frequency for time
    t = n / fs
    return t

# Get the ADSR envelope
def generate_adsr(fs, T_s, attack, decay, sustain, release):
    t = get_time_vector(fs, T_s)
    corner_times  = [0, attack, attack + decay, T_s - release, T_s]
    corner_levels = [0, 1, sustain, sustain, 0]
    return t, np.interp(t, corner_times, corner_levels)
