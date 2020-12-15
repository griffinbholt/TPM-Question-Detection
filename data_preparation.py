from os import listdir, system, makedirs
from os.path import isfile, join, exists

import scipy as sp
import numpy as np
import pickle

import parselmouth as pm
from tysums import *
from henrys import *

clip_length = 5000
clip_period = 500


PATH_TO_MTC_DATA = '/srv/mtc_data'
PATH_TO_AUDIO = join(PATH_TO_MTC_DATA, 'tpm-f2020-project/mtc-audio-TRC')
PATH_TO_SPLIT_AUDIO = join(PATH_TO_MTC_DATA, 'tpm-f2020-project/mtc-split-wav-files')

SPLIT_AUDIO_DIR_CONVENTION = 'length-{}-period-{}'
DATA_POINT_DIR_CONVENTION = 'starttime-{}-title-{}'
SPLIT_AUDIO_FILE_CONVENTION = 'last-{}.wav'
QUESTION_TRUTH_LABELS_CONVENTION = 'tpm-f2020-project/length-{}-period-{}-question_truth_labels.pkl'

f = open(join(PATH_TO_MTC_DATA, 'tpm-f2020-project/batches_dirs.pkl'), "wb")
batches_dirs = pickle.load(f)
f.close()

f = open(join(PATH_TO_MTC_DATA, 'tpm-f2020-project/batches_labels.pkl'), "wb")
batches_labels = pickle.load(f)
f.close()

data_matrix = []
labels_array = []

for i in range(len(batches_dirs)):
    batch_dirs = batches_dirs[i]
    batch_labels = batches_labels[i]

    for j in range(len(batch_dirs)):
        data_point_dir = batch_dirs[j]
        label = batch_labels[j]
        try:
            full_audio = pm.Sound(join(data_point_dir, SPLIT_AUDIO_FILE_CONVENTION.format(0)))

            t_end = full_audio.get_end_time()
            t_beg_last_500 = t_end - 0.5
            t_beg_last_500 = t_beg_last_500 if t_beg_last_500 > 0 else 0
            t_beg_last_200 = t_end - 0.2
            t_beg_last_200 = t_beg_last_200 if t_beg_last_200 > 0 else 0

            last_500 = full_audio.extract_part(from_time=t_beg_last_500, to_time=t_end)
            last_200 = full_audio.extract_part(from_time=t_beg_last_200, to_time=t_end)

            audio_clips = [full_audio, last_500, last_200]
            feature_vals = []

            for audio_clip in audio_clips:
                sample_freq = audio_clip.sampling_frequency

                f0 = calculate_fundemental_frequency(audio_clip)
                feature_vals.extend(get_stats(f0, sample_freq))

                signal_intensity = calculate_signal_intensity(audio_clip)
                feature_vals.extend(get_stats(signal_intensity, sample_freq))

                jitter = calculate_jitter_of_audio_clip(audio_clip)
                feature_vals.append(jitter)

                shimmer = calculate_shimmer_of_audio_clip(audio_clip)
                feature_vals.append(shimmer)

                mfcc_coeff_vectors = calculate_MFCC_coefficients(audio_clip)
                for mfcc_coeff_vector in mfcc_coeff_vectors:
                    feature_vals.extend([np.mean(mfcc_coeff_vector), np.std(mfcc_coeff_vector)])

                rms = calculate_RMS_frame_energy(audio_clip)
                feature_vals.append(rms)

            num_pauses, pause_durations, pause_starts, pause_total_length = calculate_pauses(full_audio)
            feature_vals.extend([num_pauses, pause_total_length])
            feature_vals.extend(get_pause_stats(pause_durations, pause_starts))

            zcr = calculate_zero_crossing_rate(full_audio)
            feature_vals.append(zcr)

            spectral_balance = calculate_spectral_balance(full_audio)
            feature_vals.append(spectral_balance)

            average_psd = calculate_power_spectral_density(full_audio)
            feature_vals.append(np.argmax(average_psd))
            feature_vals.append(np.max(average_psd))

            data_matrix.append(np.array(np.array(feature_vals)))
            labels_array.append(label)

full_data_matrix = np.array(data_matrix)
full_labels_array = np.array(labels_array)

f = open(join(PATH_TO_MTC_DATA, 'tpm-f2020-project/full_matrix.pkl'), "wb")
pickle.dump(full_data_matrix, f)
f.close()

f = open(join(PATH_TO_MTC_DATA, 'tpm-f2020-project/labels_array.pkl'), "wb")
pickle.dump(labels_array,f)
f.close()