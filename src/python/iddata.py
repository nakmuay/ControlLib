import numpy as np

class iddata:

    _dt = 1.0
    _expname = "Experiment"

    def __init__(self, y, u, dt=_dt, expname=_expname):
        self._y = []
        self._u = []
        self._dt = []
        self._time = []
        self._expname = [] 

        self.append(y, u, dt, expname)

    @property
    def y(self):
        return ReadOnlyList(self._y)

    @property
    def u(self):
        return ReadOnlyList(self._u)

    @property
    def dt(self):
        return ReadOnlyList(self._dt)

    @property
    def expname(self):
        return self._expname

    @property
    def num_experiments(self):
        return len(self._experiments)

    def append(self, y, u, dt=_dt, expname=_expname):
        self._y.append(y)
        self._u.append(u)

        self._dt.append(dt)
        self._time.append(np.arange(len(u)) * dt)

        self._expname.append(expname)

    def plot(self):
        from matplotlib import pyplot as plt

        for y, u, t, e in zip(self._y, self._u, self._time, self._expname):
            plt.figure()

            plt.subplot(2, 1, 1)
            plt.title(e)
            plt.plot(t, y, "r")
            plt.ylabel("y")
            plt.xlabel("time")

            plt.subplot(2, 1, 2)
            plt.plot(t, u, "b")
            plt.ylabel("u")
            plt.xlabel("time")

        plt.show()

# Taken from: https://stackoverflow.com/questions/22340576/immutable-list-in-python
class ReadOnlyList(list):
    def __init__(self, other):
        self._list = other

    def __getitem__(self, index):
        return self._list[index]

    def __iter__(self):
        return iter(self._list)

    def __slice__(self, *args, **kw):
        return self._list.__slice__(*args, **kw)

    def __repr__(self):
        return repr(self._list)

    def __len__(self):
        return len(self._list)

    def NotImplemented(self, *args, **kw):
        raise ValueError("Read Only list proxy")

    append = pop = __setitem__ = __setslice__ = __delitem__ = NotImplemented
