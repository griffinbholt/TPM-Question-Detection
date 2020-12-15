from os import listdir, system, makedirs
from os.path import isfile, join, exists

import scipy as sp
import numpy as np
import pickle
import random

clip_length = 5000
clip_period = 500

PATH_TO_MTC_DATA = '/srv/mtc_data'
PATH_TO_AUDIO = join(PATH_TO_MTC_DATA, 'tpm-f2020-project/mtc-audio-TRC')
PATH_TO_SPLIT_AUDIO = join(PATH_TO_MTC_DATA, 'tpm-f2020-project/mtc-split-wav-files')

SPLIT_AUDIO_DIR_CONVENTION = 'length-{}-period-{}'
DATA_POINT_DIR_CONVENTION = 'starttime-{}-title-{}'
SPLIT_AUDIO_FILE_CONVENTION = 'last-{}.wav'
QUESTION_TRUTH_LABELS_CONVENTION = 'tpm-f2020-project/length-{}-period-{}-question_truth_labels.pkl'

current_model_dir = join(PATH_TO_SPLIT_AUDIO, SPLIT_AUDIO_DIR_CONVENTION.format(clip_length, clip_period))
data_point_dirs = [join(current_model_dir, data_point_dir) for data_point_dir in listdir(current_model_dir)]

f = open(join(PATH_TO_MTC_DATA, QUESTION_TRUTH_LABELS_CONVENTION.format(clip_length, clip_period)), "rb")
labels_dictionary = pickle.load(f)
f.close()

labels_array_orig_order = [labels_dictionary[data_point_dir] for data_point_dir in data_point_dirs]

indices = [i for i in range(len(data_point_dirs))]
random.shuffle(indices)

batches_dirs = []
batches_labels = []
for i in range(0, len(indices), 500):
    batch_dirs = []
    batch_labels = []
    for j in range(500):
        print(i + j)
        if i + j < len(indices):
            index = indices[i + j]
            batch_dirs.append(data_point_dirs[index])
            batch_labels.append(labels_array_orig_order[index])
    batches_dirs.append(batch_dirs)
    batches_labels.append(batch_labels)

f = open(join(PATH_TO_MTC_DATA, 'tpm-f2020-project/batches_dirs.pkl'), "wb")
pickle.dump(batch_dirs,f)
f.close()

f = open(join(PATH_TO_MTC_DATA, 'tpm-f2020-project/batches_labels.pkl'), "wb")
pickle.dump(batch_dirs,f)
f.close()
