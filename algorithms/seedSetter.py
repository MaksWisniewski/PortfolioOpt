import numpy as np


class SeedSetter:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        np.random.seed(10)
        return self.func(*args, **kwargs)
