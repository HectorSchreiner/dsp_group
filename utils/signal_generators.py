import numpy as np
from utility import *


def generate_sinusoid(f, fs, T_s, phase=0, amp=1):
    t = get_time_vector(fs, T_s)
    sig = amp * np.sin(2*np.pi * (f * t + phase))
    return t, sig

def generate_square(f, fs, T_s, phase=0, amp=1, duty=0.5):
    t = get_time_vector(fs, T_s)
    sig = amp * np.where((t * f + phase) % 1 < duty, 1.0, -1.0)
    return t, sig

def generate_triangle(f, fs, T_s, phase=0, amp=1):
    t = get_time_vector(fs, T_s)
    sig = amp * (4 * np.abs((t * f + 0.75 + phase) % 1 - 0.5) - 1)
    return t, sig

def generate_sawtooth(f, fs, T_s, phase=0, amp=1):
    t = get_time_vector(fs, T_s)
    sig = amp * (2 * ((t * f + 0.5 + phase) % 1) - 1)
    return t, sig