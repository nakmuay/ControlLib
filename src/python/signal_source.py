from abc import ABCMeta, abstractmethod
from random import random 
import numpy as np

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
