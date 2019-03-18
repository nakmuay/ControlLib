import numpy as np
from robustness import assert_type, \
                       assert_not_none, \
                       assert_array_like

def _convert_data_shape(dat):
    if dat.ndim == 1:
        dat = dat[:, None]
    return dat

class IdDataExperiment:
 
    def __init__(self, y, u, dt, name):
        # TODO: Do we need to check that ts is a number?
        self._y = _convert_data_shape(y)
        self._u = _convert_data_shape(u)
        self._dt = dt
        self._time = np.array(range(len(u)))*dt
        self._name = name

    @property
    def y(self):
        return self._y

    @property
    def u(self):
        return self._u

    @property
    def dt(self):
        return self._dt

    @property
    def time(self):
        return self._time

    @property
    def num_outputs(self):
        if self._y.ndim == 0:
            return 0
        else:
            return self._y.shape[1]

    @property
    def num_inputs(self):
        if self._u.ndim == 0:
            return 0
        else:
            return self._u.shape[1]

    @property
    def num_samples(self):
        return len(self.u)

    @property
    def name(self):
        return self._name

    @property
    def shape(self):
        # TODO: Update shape when support for multiple input/output channels are added
        return (self.num_samples, self.num_outputs, self.num_inputs)

    def plot(self):
        from matplotlib import pyplot as plt
        print(self.y)

        plt.subplot(2, 1, 1)
        plt.title(self.name)
        plt.plot(self.time, self.y, "r")
        plt.ylabel("y")
        plt.xlabel("time")

        plt.subplot(2, 1, 2)
        plt.plot(self.time, self.u, "b")
        plt.ylabel("u")
        plt.xlabel("time")


class IdData:

    _dt = 1.0
    _expname = "Experiment"

    def __init__(self, y, u, dt=_dt, expname=_expname):
        self._experiments = []
        self.append(y, u, dt, expname)

    @property
    def y(self):
        exp_y = [exp.y for exp in self._experiments]
        return ReadOnlyList(exp_y)

    @property
    def u(self):
        exp_u = [exp.u for exp in self._experiments]
        return ReadOnlyList(exp_u)

    @property
    def dt(self):
        exp_dt = [exp.dt for exp in self._experiments]
        return ReadOnlyList(exp_dt)

    @property
    def time(self):
        exp_time = [exp.time for exp in self._experiments]
        return ReadOnlyList(exp_time)

    @property
    def expname(self):
        exp_name = [exp.name for exp in self._experiments]
        return ReadOnlyList(exp_name)

    @property
    def num_experiments(self):
        return len(self._experiments)

    @property
    def shape(self):
        exp_num_samples = [exp.num_samples for exp in self._experiments]
        (_, num_outputs, num_inputs) = self._experiments[0].shape
        return (exp_num_samples, num_outputs, num_inputs, self.num_experiments)
 
    def append(self, y, u, dt=_dt, expname=_expname):
        assert_not_none(y)
        assert_array_like(y)
        assert_not_none(u)
        assert_array_like(u)

        exp = IdDataExperiment(np.array(y), np.array(u), dt, expname)
        self._experiments.append(exp)

    def plot(self):
        from matplotlib import pyplot as plt

        for e in self._experiments:
            plt.figure()
            e.plot()

# Taken from: https://stackoverflow.com/questions/22340576/immutable-list-in-python
class ReadOnlyList(list):
    def __init__(self, other):
        self._list = other

    def __getitem__(self, index):
        return self._list[index]

    def __iter__(self):
        return iter(self._list)

    def __slice__(self, *args, **kwargs):
        return self._list.__slice__(*args, **kwargs)

    def __repr__(self):
        return repr(self._list)

    def __len__(self):
        return len(self._list)

    def NotImplemented(self, *args, **kwargs):
        raise ValueError("Read Only list proxy")

    append = pop = __setitem__ = __setslice__ = __delitem__ = NotImplemented
