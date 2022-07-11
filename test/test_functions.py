import numpy as np

from gaga.functions import *

def test_softmax():
    assert np.array_equal(softmax([1,1]),[0.5, 0.5])
