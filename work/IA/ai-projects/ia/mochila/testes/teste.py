

class Item(object):
    def __init__(self, v, w):
        self.value = v # Item's value. You want to maximize that!
        self.weight = w # Item's weight. The sum of all items should be <= CAPACITY



ITEMS = [
    Item(1, 3), Item(3, 8), Item(1, 12), Item(8, 2), Item(9, 8), Item(3, 4), Item(2, 4), Item(8, 5), Item(5, 1), Item(1, 1)
    , Item(1, 8), Item(6, 6), Item(3, 4), Item(2, 3), Item(5, 3), Item(2, 5), Item(7, 3), Item(8, 3), Item(9, 5), Item(3, 7)
    , Item(2, 4), Item(4, 3), Item(5, 7), Item(4, 2), Item(3, 3), Item(1, 5), Item(3, 4), Item(2, 3), Item(14, 7), Item(32, 19)
    , Item(20, 20), Item(19, 21), Item(15, 11), Item(37, 24), Item(18, 13), Item(13, 17), Item(19, 18), Item(10, 6)
    , Item(15, 5), Item(40, 25), Item(17, 12), Item(39, 19)
]

CAPACITY = 113

import numpy as np

def fitness():

    total_value = 0
    total_weight = 0
    index = 0
    for i in np.arange(1,42):
        total_value += ITEMS[i].value
        total_weight += ITEMS[i].weight
    print(total_weight)
    print(total_value)


fitness()