from abc import ABCMeta, abstractmethod
from random import random 
import numpy as np
from scipy.signal import windows, \
                         convolve

from iddata import IdData 

class SignalModifier(metaclass=ABCMeta):
    """
    Interface for signal source modifiers
    """

    def apply(self, source):
        if (isinstance(source, IdData)):
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

    def apply(self, dat):
        if (type(dat), type(IdData)):
            return self._apply_iddata(dat)
        return self._apply_core(dat)

    def _apply_core(self, signal):
        w = windows.gaussian(self._window_size, self._std, sym=True)
        return convolve(signal, w, mode='same') / sum(w)

class SignalSource(metaclass=ABCMeta):
    """
    Interface for signal sources
    """

    @abstractmethod
    def generate(self):
        pass

class SinSource(SignalSource):

    def __init__(self, num_samples,  amplitude=1.0, frequency=1.0, phase_shift=0.0):
        self._num_samples = num_samples
        self._amplitude = amplitude
        self._frequency = frequency
        self._phase_shift = phase_shift

    def generate(self):
        time_vector = np.array(range(self._num_samples))
        signal = self._amplitude * np.sin(2.0*np.pi * self._frequency * time_vector + self._phase_shift)
        return signal

class CompoundSource(SignalSource):

    def __init__(self, sources):
        self._sources = sources
        
    def generate(self):
        signal = self._sources[0].generate()
        for source in self._sources:
            signal = signal + source.generate()
        return signal

class RandCompoundSource(SignalSource):

    def __init__(self, sources):
        self._sources = sources
        
    def generate(self):
        signal = random()*self._sources[0].generate()
        for source in self._sources:
            signal = signal + random()*source.generate()
        return signal

class IdDataFactory(metaclass=ABCMeta):
    """
    Identification data factory interface
    """

    @abstractmethod
    def create(self, num_samp):
        pass

class TwoInputSignalsIdDataFactory(IdDataFactory):

    def __init__(self, num_samp):
        in_signal = np.array(range(num_samp))
        self._in_signals = np.vstack((in_signal, 10*in_signal)).T
        self._out_signal = np.array(range(num_samp)).T

    def create(self):
        return IdData(self._out_signal, self._in_signals)

class FlightIdDataFactory(IdDataFactory):

    def __init__(self, num_samp):
        self._num_samp = num_samp
        generator = RandCompoundSource([
                                    SinSource(self._num_samp, amplitude=1.5, frequency=1.0/100.0, phase_shift=3.0),
                                    SinSource(self._num_samp, amplitude=1.0, frequency=1.0/50.0),
                                    SinSource(self._num_samp, amplitude=0.5, frequency=1.0/30.0),
                                    SinSource(self._num_samp, amplitude=0.25, frequency=1.0/20.0),
                                    ])
        self._generator = generator

    def create(self):
        # generate a signal
        in_signal = self._generator.generate()
        noise_modifier = GaussianNoiseModifier(0.04)
        in_signal = noise_modifier.apply(in_signal)

        # normalize signal
        norm_modifier = NormalizingModifier()
        in_signal = norm_modifier.apply(in_signal)

        # add some noise to output
        out_signal = in_signal + 0.5*SinSource(self._num_samp, amplitude=1.0, frequency=1.0/60.0).generate()
        out_signal = noise_modifier.apply(out_signal)
        
        # normalize output
        out_signal = norm_modifier.apply(out_signal)

        # create identification data
        dat = IdData(out_signal, in_signal)
        return dat