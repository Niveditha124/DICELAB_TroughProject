import numpy as np


def weedmark_ext(field_w): #generic extension function
    o_w = (field_w.shape[1]) + 2
    dx = field_w[0, 1] - field_w[0, 0]
    extended_field = np.zeros((1, o_w), float)
    extended_field[0, 0] = field_w[0, 0] - dx
    for p in range(0, o_w-2):
        extended_field[0, p + 1] = field_w[0, p]
    extended_field[0, o_w-1] = field_w[0, o_w-3] + dx
    return extended_field
