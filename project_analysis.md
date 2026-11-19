# Project analysis – Space travel (22051)

## The deliverable

You need a **40–60 s stereo WAV** (44.1 kHz or higher, 16 bit or more) of spaceship radio audio, plus:

- the code: a main notebook (35%) and filter/effect modules (25%)
- a short technical report as a PDF (10%)
- a **5-minute video** (10%)

The final audio track itself counts for 20%. Everything goes in `GRP_#_group_assignment.zip`, due in week 13.

In the video you must pick **3 elements** (one per group member) and for each one:
1. justify the design choice and show what a wrong choice would do,
2. name an alternative and its impact,
3. say where you got stuck, if anywhere.

## Scenes, owners and the DSP concepts each one should show

Owners are taken from `main.ipynb`. The concepts come from Tables A.1, A.2 and A.5 in the brief.

| # | Scene (owner) | What's heard | Concepts to put here |
|---|---|---|---|
| 0 | **Camera feed** (together) | Mirrored ship name shown on screen | Image flipping, reused from the "Sound is art" individual assignment |
| 1 | **Calm transmission** (Halfdan) | Clean synth music (from "Add/multiply/synthesize"), optional ship hum | **Choice of sampling rate with a Nyquist argument** (LO1). **Anti-aliasing filter before resampling** and the minimum workable rate (LO9). Reference spectrogram |
| 2 | **Instrument detection** (Hector) | A *recorded* instrument, the detector working, optional device beep, and a readout like "belongs to the group of …" | Harmonic analysis and **spectral centroid**, a classification demo with an **accuracy metric** (LO5). Also the natural place for **frequency resolution**: the brief's joke about the guy who thought raising fs improves resolution. Link Δf = fs/N = 1/T_window to DFT length and window choice |
| 3 | **Gradual interference** (Marcus) | Narrowband noise at 6–8 kHz fading in, then removed | **FIR band-stop** with coefficients and frequency response (LO3). **IIR band-stop via the bilinear transform with pre-warping worked out in code** (LO4). The IIR is the obvious filter for the **pole-zero plot and stability discussion**. Spectrograms before and after filtering |
| 4 | **Sudden degradation** (Marcus) | Broadband hiss/crackle plus the first drop-outs | **Broadband noise generator with spectral shaping** (LO6). **PSD with Welch or a periodogram**, with justified segment length, overlap and window (LO5/6) |
| 5 | **Moon-shadow entry and blackout, about 2 s** (Hector) | Half the bandwidth, fewer bits, more drop-outs, then full silence | **Windowing and attenuation curves for the fade-out** (Hann/Hamming/Blackman, justified) (LO7). **Reduced quantisation: bit depth vs SNR** (about 6 dB per bit) with an audio comparison (LO1/9). **Halving the bandwidth means decimation**, so an anti-aliasing filter is needed. **Interpolation over drop-outs** (linear, spline or cubic) (LO3) |
| 6 | **Recovery** (Halfdan) | Signal comes back in steps | **Crossfades and envelopes that avoid clicks** (LO7/10). **Effects of resampling back up**, with an FFT vs DTFT vs DFT explanation (LO2) |
| 7 | **Return to normal** (Halfdan) | Clean news feed | Final spectrogram that matches scene 1 |
| — | **Integration and documentation** (together) | — | Pipeline that runs end to end (LO10). **Spectrograms of every scene phase**. Consistent DSP terminology (LO11). **At least 2 cited sources** for the filter design choices (LO12) |

**Coverage check against the mandatory list (A.2):** FIR and IIR (scene 3), bilinear transform with pre-warping (3), PSD (4), pole-zero plot (3, or any IIR you use), spectrograms (all scenes), fs/Nyquist (1), frequency resolution (2, with the PSD window length in 4), terminology and citations (documentation). As long as each item is clearly documented somewhere, it is covered.

## How the individual "Tune in!" assignment feeds into scene 2

The individual assignment is due in week 10. Its parts carry over almost directly:

| Individual component | Use in the group project |
|---|---|
| f0 estimator (autocorrelation, HPS, YIN, …) | Detect the pitch of the instrument recording; the detector "display" |
| Harmonic analysis (harmonic amplitudes, spectral centroid, inharmonicity) | The spectral features the brief asks for in this scene (LO5) |
| Temporal analysis (ADSR envelope, attack time, zero-crossing rate) | Extra features that separate plucked, bowed and blown sounds |
| Feature vector and classifier | Output the instrument **family** (strings, woodwind, brass, keyboard or percussion). That is the brief's "group of <YOU FIGURE IT OUT>" |
| Deviation indicator (cents = 1200·log₂(f/f_ref)) | Optional on-screen or audio feedback, e.g. a beep from the "device" |
| Classification accuracy on several recordings | Gives you the accuracy metric that A.5 requires |

You can also turn the "wrong choice" part of the video into a demo. A window that is too short smears the harmonics and leads to misclassification, and raising fs without lengthening the window doesn't fix it.

## Things to agree on as a group

- **The boundary between Marcus's degradation and the blackout.** Drop-outs appear in both scenes, so decide who owns them.
- **One shared sampling rate and bit depth from start to finish.** Pick it in scene 1, and treat the reduced bits in scene 5 as a deliberate effect.
- **Which 3 elements go in the video.** Instrument detection or blackout quantisation would be strong picks.
