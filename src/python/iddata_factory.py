from abc import ABCMeta, abstractmethod
import numpy as np

from iddata import IdData 
from signal_source import SinSource, \
                            RandCompoundSource
from signal_modifier import GaussianNoiseModifier, \
                            NormalizingModifier

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