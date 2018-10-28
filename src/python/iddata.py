import numpy as np
from robustness import assert_type

class iddata_experiment:
 
    def __init__(self, y, u, ts, name):
        assert_type(y, np.ndarray)
        assert_type(u, np.ndarray)
        # TODO: Do we need to check that ts is a number?

        self._y = y
        self._u = u
        self._ts = ts
        self._time = np.array(range(len(u)))*ts
        self._name = name

    @property
    def y(self):
        return self._y

    @property
    def u(self):
        return self._u

    @property
    def ts(self):
        return self._ts

    @property
    def time(self):
        return self._time

    @property
    def name(self):
        return self._name

    def plot(self):
        from matplotlib import pyplot as plt

        plt.subplot(2, 1, 1)
        plt.title(self.name)
        plt.plot(self.time, self.y, "r")
        plt.ylabel("y")
        plt.xlabel("time")

        plt.subplot(2, 1, 2)
        plt.plot(self.time, self.u, "b")
        plt.ylabel("u")
        plt.xlabel("time")


class iddata:

    _ts = 1.0
    _expname = "Experiment"

    def __init__(self, y, u, ts=_ts, expname=_expname):
        self._experiments = []
        self.append(y, u, ts, expname)

    @property
    def y(self):
        exp_y = [exp.y for exp in self._experiments]
        return ReadOnlyList(exp_y)

    @property
    def u(self):
        exp_u = [exp.u for exp in self._experiments]
        return ReadOnlyList(exp_u)

    @property
    def ts(self):
        exp_ts = [exp.ts for exp in self._experiments]
        return ReadOnlyList(exp_ts)

    @property
    def expname(self):
        exp_name = [exp.name for exp in self._experiments]
        return ReadOnlyList(exp_name)

    @property
    def num_experiments(self):
        return len(self._experiments)

    def append(self, y, u, ts=_ts, expname=_expname):
        exp = iddata_experiment(y, u, ts, expname)
        self._experiments.append(exp)

    def plot(self):
        from matplotlib import pyplot as plt

        for e in self._experiments:
            plt.figure()
            e.plot()

        plt.show()

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

    def NotImplemented(self, *args, **kw):
        raise ValueError("Read Only list proxy")

    append = pop = __setitem__ = __setslice__ = __delitem__ = NotImplemented
