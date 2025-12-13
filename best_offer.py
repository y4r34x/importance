import pandas as pd
import numpy as np

def equations(x: None, avgs: np.array, set_equity: float = 0.3):
  
  c, v = x
  avg_score = avgs[0]
  avg_ratio = avgs[1]

  # equation 1: avg_score = e/vc^2, equation 2: avg_ratio = c/v
  eq1 = avg_score - set_equity / (c ** 2 * v)
  eq2 = c - avg_ratio * v

  return [eq1, eq2]

