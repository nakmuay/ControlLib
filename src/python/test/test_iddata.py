import unittest
import os
import sys
import numpy as np
from numpy import testing as np_test

sys.path.append("/home/martin/src/ControlLib/src/python")
from iddata import IdData

class TestIdDataInit(unittest.TestCase):

    def setUp(self):
        self.input_data = np.array([[1.0, 1.1], [2.0, 2.2], [3.0, 3.3]])
        self.output_data = np.array([[10.0, 10.1], [20.0, 20.2], [30.0, 30.3]])
        self.data = IdData(self.output_data, self.input_data) 

    def test_y_none_error(self):
        self.assertRaises(ValueError, IdData, None, self.input_data, dt=1.0)

    def test_u_none_error(self):
        self.assertRaises(ValueError, IdData, self.output_data, None, dt=1.0)

    def test_y_copy_on_initialization(self):
        y = np.array(range(3))
        u = np.array(range(3))
        dat = IdData(y, u, dt=1.0)
        y[0] = 100.0

        np_test.assert_almost_equal(dat.y[0], np.array(range(3)))

    def test_u_copy_on_initialization(self):
        y = np.array(range(3))
        u = np.array(range(3))
        dat = IdData(y, u, dt=1.0)
        u[0] = 100.0

        np_test.assert_almost_equal(dat.u[0], np.array(range(3)))

    def test_array_like_assert(self):
        self.assertRaises(ValueError, IdData, 0.0, np.array(range(3)))
        self.assertRaises(ValueError, IdData, np.array(range(3)), 0.0)

if __name__ == "__main__":
    unittest.main()
