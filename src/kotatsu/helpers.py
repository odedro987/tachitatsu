import numpy as np

ID_SEED = 1125899906842597


def get_kotatsu_id(str):
    h = np.int64(ID_SEED)
    for c in str:
        h = np.add(np.multiply(np.int64(31), h), np.int64(ord(c)))
    return h
