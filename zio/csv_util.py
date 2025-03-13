from pandas import DataFrame
import numpy as np


def test_generate_cvs_data():
    print()
    data = DataFrame(np.zeros((2, 5)), columns=['a', 'b', 'c', 'd', 'e'])
    data.to_csv('tmp/tmp.csv')
    list = []
    for i in range(5):
        list.append((None, 1, None, 2, None))
    data = DataFrame(list, columns=['a', 'b', 'c', 'd', 'e'])
    data.to_csv('tmp/tmp2.csv')
