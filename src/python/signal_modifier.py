from abc import ABCMeta, abstractmethod
import numpy as np
from scipy.signal import windows, \
                         convolve

from iddata import IdData

class SignalModifier(metaclass=ABCMeta):
    """
    Interface for signal source modifiers
    """

    def apply(self, source):
        if isinstance(source, IdData):
            return self._apply_iddata(source)
        return self._apply_core(source)

    def _apply_iddata(self, dat):
        u = self._apply_core(dat.u[0][:, 0])
        y = self._apply_core(dat.y[0][:, 0])
        dt = dat.dt
        return IdData(u, y, dt=dt)

    @abstractmethod
    def _apply_core(self, signal):
        pass

class GaussianNoiseModifier(SignalModifier):
    """
    Class which adds gaussian noise to a signal
    """

    def __init__(self, std=1.0):
        self._std = std

    def _apply_core(self, signal):
        signal = signal + np.random.normal(0.0, self._std, len(signal))
        return signal

class NormalizingModifier(SignalModifier):
    """
    Class which normalizes a signal
    """

    def __init__(self):
        self._name = "Normalizing modifier"

    def _apply_core(self, signal):
        # remove mean
        signal = signal - np.mean(signal)
        denominator = np.max(np.abs(signal))
        if denominator == 0.0:
            print("Division by zero!")
        signal = signal / denominator
        return signal

class SmoothingModifier(SignalModifier):
    """
    Class which smooths a signal
    """

    def __init__(self, window_size=3, std=1.0):
        self._name = "Smoothing modifier"
        self._window_size = window_size
        self._std = std

    def _apply_core(self, signal):
        w = windows.gaussian(self._window_size, self._std, sym=True)
        return convolve(signal, w, mode='same') / sum(w)
