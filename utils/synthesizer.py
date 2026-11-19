from signal_generators import *
from utility import *
from filters import *
from IPython.display import Audio, display
from scipy.io import wavfile
from dataclasses import dataclass, field
from typing import Literal
from __future__ import annotations
from matplotlib import pyplot as plt


# Dataclass for containing configuration parameters of an oscillator
@dataclass(frozen=True)
class OscillatorConfiguration:
    const: float
    coef: float
    channel: ChannelConfiguration # type: ignore


# Dataclass for containing configuraiton parameters of an ADSR envelope
@dataclass(frozen=True)
class ADSRConfiguration:
    attack: float
    decay: float
    sustain: float
    release: float


# Dataclass for containing configuration paramters of a single filter
@dataclass(frozen=True)
class FilterConfiguration:
    filter_type: Literal[
        "lowpass",
        "highpass",
        "bandpass",
        "allpass"
    ]
    start_freq: float | OscillatorConfiguration = 0.0
    stop_freq: float | OscillatorConfiguration = 0.0
    a: int = 0.0
    order: int = 4


# Dataclass for containing configuration parameters of a single channel
@dataclass(frozen=True)
class ChannelConfiguration:
    type: Literal["sinusoid", "square", "triangle", "sawtooth"]
    freq: float
    amp: float = 1.0
    phase: float = 0.0
    duty: float = 0.5
    filters: list[FilterConfiguration] = field(default_factory=list)
    adsr: ADSRConfiguration | None = None


# Main dataclass for containing all the synthesizer configuraiton parameters
@dataclass(frozen=True)
class SynthesizerConfiguration:
    fs: int = 44100
    T_s: float = 1.0
    channels: list[ChannelConfiguration] = field(default_factory=list)
    filters: list[FilterConfiguration] = field(default_factory=list)
    adsr: ADSRConfiguration | None = None


class Synthesizer:
    def __init__(self, config):
        self.config = config
        self.generated_signals = []
        self.adsr_envelopes = []
        self.adsr_signals = []
        self.filtered_signals = []

    # Generate the sound specified from the provided configuration
    def generate(self):
        self.t  = get_time_vector(self.config.fs, self.config.T_s)

        # Generate channel signals
        for channel in self.config.channels:
            sig = self.get_generated_signal(channel)

            self.generated_signals.append(sig)

            envelope = np.array([1 for _ in range(len(self.t))])
            if channel.adsr != None:
                adsr_config = channel.adsr
                _, envelope = generate_adsr(self.config.fs, self.config.T_s, adsr_config.attack, adsr_config.decay, adsr_config.sustain, adsr_config.release)
                sig = sig * envelope
            self.adsr_envelopes.append(envelope)
            self.adsr_signals.append(sig)

            for filter in channel.filters:
                sig = self.get_filtered_signal(filter, sig)
            self.filtered_signals.append(sig)

        # Sum signals
        self.sum_signal = np.array(sum(self.filtered_signals))
        self.sum_signal = self.sum_signal / np.max(self.sum_signal)

        self.sum_adsr_signal = self.sum_signal
        self.sum_envelope = np.array([1 for _ in range(len(self.t))])
        if self.config.adsr != None:
            adsr_config = self.config.adsr
            _, self.sum_envelope = generate_adsr(self.config.fs, self.config.T_s, adsr_config.attack, adsr_config.decay, adsr_config.sustain, adsr_config.release)
            self.sum_adsr_signal = self.sum_signal * self.sum_envelope

        self.sum_filtered_signal = self.sum_adsr_signal
        for filter in self.config.filters:
            self.sum_filtered_signal = self.get_filtered_signal(filter, self.sum_filtered_signal)

        # Save the output signal and make it playable for the user
        wavfile.write("sounds/synth_sound.wav", self.config.fs, self.sum_filtered_signal.astype(np.float32))
        display(Audio(data=f"sounds/synth_sound.wav"))


    # Plot data from selected stages of the signal generation
    def show_plot(self):
        fig = plt.figure(figsize=(20, 10), layout="constrained")
        gs = fig.add_gridspec(8, len(self.config.channels))

        top_axes = []
        for i in range(len(self.config.channels)):
            column = []
            for j in range(4):
                ax = fig.add_subplot(gs[j, i])
                ax.set_ylim(-1.2, 1.2)
                match j:
                    case 0:
                        ax.plot(self.t, self.generated_signals[i], color="black")
                        ax.set_title(f"Generated signal (channel {i+1})")
                    case 1:
                        ax.plot(self.t, self.adsr_envelopes[i], color="black")
                        ax.set_title(f"ADSR envelope (channel {i+1})")
                        ax.set_ylim(-0.2, 1.2)
                    case 2:
                        ax.plot(self.t, self.adsr_signals[i], color="black")
                        ax.set_title(f"Signal with envelope (channel {i+1})")
                    case 3:
                        ax.plot(self.t, self.filtered_signals[i], color="black")
                        ax.set_title(f"Filtered signal (channel {i+1})")
                column.append(ax)
            top_axes.append(column)

        bottom_axes = []
        for i in range(4):
            ax = fig.add_subplot(gs[4+i, 0:len(self.config.channels)])
            ax.set_ylim(-1.2, 1.2)
            match i:
                case 0:
                    ax.plot(self.t, self.sum_signal, color="b")
                    ax.set_title("Sum signal")
                case 1:
                    ax.plot(self.t, self.sum_envelope, color="b")
                    ax.set_title("ADSR envelope")
                    ax.set_ylim(-0.2, 1.2)
                case 2:
                    ax.plot(self.t, self.sum_adsr_signal, color="b")
                    ax.set_title("Sum signal with envelope")
                case 3:
                    ax.plot(self.t, self.sum_filtered_signal, color="b")
                    ax.set_title("Filtered sum signal")
            bottom_axes.append(ax)

        plt.suptitle("Full synthesis plot", fontsize=14)
        plt.show()


    # Generate a signal based on a channel configuration
    def get_generated_signal(self, channel):
        match channel.type:
            case "sinusoid":
                _, sig = generate_sinusoid(channel.freq, self.config.fs, self.config.T_s, channel.phase, channel.amp)
            case "square":
                _, sig = generate_square(channel.freq, self.config.fs, self.config.T_s, channel.phase, channel.amp, duty=channel.duty)
            case "triangle":
                _, sig = generate_triangle(channel.freq, self.config.fs, self.config.T_s, channel.phase, channel.amp)
            case "sawtooth":
                _, sig = generate_sawtooth(channel.freq, self.config.fs, self.config.T_s, channel.phase, channel.amp)
        return sig


    # Filter a signal based on a filter configuration
    def get_filtered_signal(self, filter, sig):

        # In the case cutoff is given as an oscillator configuration generate a signal for that parameter
        if type(filter.start_freq) == float or type(filter.start_freq) == int:
            start_freq = [filter.stop_freq for _ in range(len(sig))]
        if isinstance(filter.start_freq, OscillatorConfiguration):
            oscillator = filter.start_freq
            start_freq = oscillator.const + oscillator.coef * self.get_generated_signal(oscillator.channel)

        if type(filter.stop_freq) == float or type(filter.stop_freq) == int:
            stop_freq = [filter.stop_freq for _ in range(len(sig))]
        if isinstance(filter.stop_freq, OscillatorConfiguration):
            oscillator = filter.stop_freq
            stop_freq = oscillator.const + oscillator.coef * self.get_generated_signal(oscillator.channel)

        match filter.filter_type:
            case "lowpass":
                sig, _ = lowpass_butter(sig, self.config.fs, start_freq, filter.order)
            case "highpass":
                sig, _ = highpass_butter(sig, self.config.fs, stop_freq, filter.order)
            case "bandpass":
                sig, _ = bandpass_butter(sig, self.config.fs, tuple(zip(start_freq, stop_freq)), filter.order)
            case "allpass":
                sig, _ = allpass(sig, filter.a)
        return sig
            