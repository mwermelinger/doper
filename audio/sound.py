"""
sound.py - play multi-channel sounds and plot their sound waves

A mono sound is represented as a list of floating-point numbers within range [-1, 1].
A stereo sound is represented as a list with two mono sounds, i.e.
as a list of two lists of floats in the range [-1, 1].
Both lists must have the same length.
More generally, an n-channel sound is represented as a list of n lists,
all of the same length and all with floats in the range [-1, 1].
"""

import array
import wave
from typing import Tuple

import matplotlib.pyplot as plt
from IPython.display import Audio

def channels(sound: list) -> int:
    """Return the number of channels."""
    if sound == [] or isinstance(sound[0], float):
        return 1
    else:
        return len(sound)

def samples(sound: list) -> int:
    """Return the number of samples in sound."""
    if channels(sound) == 1:
        return len(sound)
    else:
        return len(sound[0])

def play(sound: list, rate: int, start:int=0, end:int=0) -> Audio:
    """Create an audio player for sound, from sample start to sample end.

    If end is 0 (the default value), play until the last sample.
    """
    if start != 0 or end != 0:
        if end == 0:
            end = samples(sound)
        if channels(sound) == 1:
            sound = sound[start:end]
        else:
            sound = [channel[start:end] for channel in sound]
    return Audio(sound, rate=rate, normalize=False, embed=True)

def show(sound, start:int=0, end:int=0, title: str='') -> None:
    """Display one wave per channel in sound, from sample start to sample end."""
    plt.title(title)
    plt.xlabel('sample')
    plt.ylabel('displacement')
    if end == 0:
        end = samples(sound)
    plt.xlim(start, end)
    if channels(sound) == 1:
        plt.plot(sound)
    elif channels(sound) == 2:
        plt.plot(sound[0], label='left')
        plt.plot(sound[1], label='right')
        plt.legend()
    else:
        for index, channel in enumerate(sound):
            plt.plot(channel, label=f'channel {index}')
        plt.legend()
    plt.show()

def load(filename: str) -> Tuple[list, int]:
    """Return the samples and sampling rate of the sound in the given file.

    filename must be the name of an uncompressed 16-bit mono or stereo WAV file
    """
    with wave.open(filename, 'rb') as wav:
        if wav.getsampwidth() != 2:
            raise ValueError("WAV file doesn't use 16-bit samples")

        rate = wav.getframerate()
        bytes = wav.readframes(wav.getnframes())
        # convert every 2 bytes to a signed 16-bit integer
        integers = array.array('h', bytes)
        floats = [i / 32768 for i in integers]
        if wav.getnchannels() == 1:     # mono sound
            sound = floats
        else:                           # stereo sound
            left = floats[::2]
            right = floats[1::2]
            sound = [left, right]
    return sound, rate