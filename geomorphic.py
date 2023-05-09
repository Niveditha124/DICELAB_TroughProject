# ENTRAINMENT operator accounting for water entrainment at the top of turbidity current
# solved implicitly with backward Euler scheme (solution obtained
# interatively from the explicit estimate with a Newton scheme)
import numpy as np

def geomorphic(field, par, dt):
