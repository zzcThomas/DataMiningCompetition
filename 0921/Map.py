from math import *
import numpy as np

REG_DIM = 1000 # dimension of logistic regression
FREQ_PATH = "tmp_app_install/app_freq.npy"
TOTAL_FILES = 600
MIN_USERS = 10000
MAX_USERS = 400000
NUM_PROCESSES = 25
POPULATION_RATIO = 0.001
LOAD_PATTERN = 'contest_dataset_url/part-r-%05d'
SAVE_PATTERN = "tmp_url/feature-%d.npy"
ALL_DISTRIBUTION_PATH = 'all_dist.npy'

MAX_APPS = 2000000

freqs = np.load(FREQ_PATH).item()
freq_gender = freqs['gender']
freq_age = freqs['age']

freqs = np.load(ALL_DISTRIBUTION_PATH).item()
all_gender = freqs['gender']
all_age = freqs['age']

params = []
start = 0
for i in range(NUM_PROCESSES):
    x = (TOTAL_FILES - start) // (NUM_PROCESSES - i)
    params += [(i, start, start + x)]
    start += x
# print params

gender_dists = []
age_dists = []
for item_id in freq_gender.keys():
    gender, age = freq_gender[item_id], freq_age[item_id]
    if sum(gender) < MIN_USERS or sum(gender) > MAX_USERS:
        continue
    population = sum(gender)
    gender = gender / population
    age = age / population
    
    extra = log(population) * POPULATION_RATIO
    gender_dists += [(np.sum(gender * np.log(gender / all_gender + 1e-10)) + extra, item_id)]
    age_dists += [(np.sum(age * np.log(age / all_age + 1e-10)) + extra, item_id)]

gender_dists = list(reversed(sorted(gender_dists)))[:REG_DIM]
age_dists = list(reversed(sorted(age_dists)))[:REG_DIM]

good_age = {}
good_gender = {}
for i, (costs, item_id) in enumerate(gender_dists):
    good_gender[item_id] = i
for i, (costs, item_id) in enumerate(age_dists):
    good_age[item_id] = i

np.save("tmp_app_install/good_apps", {'gender': good_gender, 'age': good_age})

exit()

# for each user, which items does he visit? 

def load_user_item(params):
    global REG_DIM
    pid, lo, hi = params
    D = []
    total, useful = 0, 0
    for i in range(lo, hi):
        fn = LOAD_PATTERN % (i)
        print fn
        with open(fn) as fin:
            for x in fin:
                user_id, item_id, time = x.split()
                item_id = int(item_id) - 1
                total += 1
                if item_id in good_gender or item_id in good_age:
                    useful += 1
                    D += [(user_id, item_id)]
    np.save(SAVE_PATTERN % (pid), D)
    print "ratio = %d/%d ~ %.6f" % (total, useful, 1. * useful / total)
#     return D

# all_results = pool.map(load_user_item, params)
import sys
if len(sys.argv) <= 1:
    exit()
load_user_item(params[int(sys.argv[1])])
