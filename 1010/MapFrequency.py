import numpy as np
import sys

TOTAL_FILES = 163
NUM_PROCESSES = 25
MAX_KEYWORDS = 5000000
SAVE_PATTERN = "tmp_query/freq-%d"
LOAD_PATTERN = "contest_dataset_query/part-r-%05d"

params = []
start = 0
for i in range(NUM_PROCESSES):
    x = (TOTAL_FILES - start) // (NUM_PROCESSES - i)
    params += [(i, start, start + x)]
    start += x
# print params

if len(sys.argv) < 2:
    exit()

pid = int(sys.argv[1])

_, lo, hi = params[pid]

D = {}
freq_gender = np.zeros((MAX_KEYWORDS, 2))
freq_age = np.zeros((MAX_KEYWORDS, 7))

# get labels
def read_user_labels():
    user_labels = {}

    for fn in ['contest_dataset_label/label000000_0', 'contest_dataset_label/label000001_0']:
        with open(fn) as file_user_label:
            for x in file_user_label:
                user_id, gender, user_age = x.split()
                user_labels[user_id] = [int(gender) - 1, int(user_age) - 1]
    return user_labels

user_labels = read_user_labels()
print 'user labels loaded'

for i in range(lo, hi):
    file_name = LOAD_PATTERN % (i)
    print file_name
    with open(file_name) as fn:
        for x in fn:
            try:
                user_id, queries, _ = x.split()
            except:
                print x
                continue
            if user_id not in user_labels:
                continue
            if user_id not in D:
                D[user_id] = {}
            gender, age = user_labels[user_id]
            for keyword in queries.split(','):
                keyword = int(keyword) - 1
                if keyword not in D[user_id]:
                    D[user_id][keyword] = True
                    freq_gender[keyword][gender] += 1
                    freq_age[keyword][age] += 1

np.save(SAVE_PATTERN % (pid), {'gender': freq_gender, 'age': freq_age})

