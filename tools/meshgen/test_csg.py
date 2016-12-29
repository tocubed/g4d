from csg import *
from brushes import *
import numpy as np

if __name__ == '__main__':
    brush = hypercube()

    for i in range(100):
        translation = np.random.normal(size=4)
        brush = brush.union(brush.translate(translation))
        print(len(brush.polytopes))
