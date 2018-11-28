import numpy as np
import matplotlib.pyplot as plt
import math
from sklearn.linear_model import LinearRegression
from numpy.linalg import inv
from numpy import dot,transpose
import pandas as pd

np.random.seed(1234)
d1 = pd.Series(2*np.random.normal(size = 100)+3)
d2 = np.random.f(2,4,size = 100)
d3 = np.random.randint(1,100,size = 100)
#aa
