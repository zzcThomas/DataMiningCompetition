import numpy as np

SAVE_PATH = 'tmp_app_install/all-features'
LOAD_PATH = "tmp_app_install/feature-%d.npy"

def load_item_feature():
    D = {}
    for i in range(25):
        print i
        x = np.load(LOAD_PATH % (i))
        for key, val in x:
            if key not in D:
                D[key] = []
            D[key] += [val]
    return D

item_features = load_item_feature()
np.save(SAVE_PATH, item_features)
