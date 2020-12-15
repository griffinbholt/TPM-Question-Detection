# Initial Input: a list of .mp4 videos & 30 .xml files

from xml.dom import minidom

from os import listdir, system, makedirs
from os.path import isfile, join, exists

from pydub import AudioSegment

import numpy as np
import pickle

def get_millisec(time_str):
    h, m, s = time_str.split(':')
    return (int(h) * 3600 + int(m) * 60 + int(s)) * 1000

PATH_TO_MTC_DATA = '/srv/mtc_data'
PATH_TO_ANNOTATIONS = join(PATH_TO_MTC_DATA, 'annotations')
PATH_TO_VIDEOS = join(PATH_TO_MTC_DATA, 'mtc-videos-TRC')
PATH_TO_AUDIO = join(PATH_TO_MTC_DATA, 'tpm-f2020-project/mtc-audio-TRC')
PATH_TO_SPLIT_AUDIO = join(PATH_TO_MTC_DATA, 'tpm-f2020-project/mtc-split-wav-files')

SPLIT_AUDIO_DIR_CONVENTION = 'length-{}-period-{}'
DATA_POINT_DIR_CONVENTION = 'starttime-{}-title-{}'
SPLIT_AUDIO_FILE_CONVENTION = 'last-{}.wav'
QUESTION_TRUTH_LABELS_CONVENTION = 'tpm-f2020-project/length-{}-period-{}-question_truth_labels.pkl'

XML_TAG_NAME = 'video'
FILENAME_ATTR = 'filename'
QUESTION_TRUTH_ATTR = 'question_truth'

MP4_FORMAT = 'mp4'
WAV_FORMAT = 'wav'

CLIP_LENGTHS = [4000, 5000] # milliseconds
CLIP_PERIODS = [100, 250, 500] # milliseconds

# Get the list of annotation XML files
annotation_files = [join(PATH_TO_ANNOTATIONS, xml_file) for xml_file in listdir(PATH_TO_ANNOTATIONS) if isfile(join(PATH_TO_ANNOTATIONS, xml_file))]

# Parse each XML file
annotations = list(map(minidom.parse, annotation_files))

# Extract the files names and the question_truth lists for each of the .mp4 videos from the XML files
mp4_filepaths, wav_files, wav_filepaths = [], [], []
question_times = {}
for annotation in annotations:
    video_elem = annotation.getElementsByTagName(XML_TAG_NAME)[0]
    mp4_filename = video_elem.attributes[FILENAME_ATTR].value.replace(MP4_FORMAT.upper(), MP4_FORMAT)
    wav_file = mp4_filename.replace(MP4_FORMAT, WAV_FORMAT)
    mp4_filename = join(PATH_TO_VIDEOS, mp4_filename)

    if mp4_filename not in mp4_filepaths:
        mp4_filepaths.append(mp4_filename)

        wav_files.append(wav_file)
        wav_filepaths.append(join(PATH_TO_AUDIO, wav_file))

    question_time_vector = list(map(get_millisec, eval(video_elem.attributes[QUESTION_TRUTH_ATTR].value)))

    if wav_file in question_times:
        question_times[wav_file].extend(question_time_vector)
        question_times[wav_file].sort()
    else:
        question_times[wav_file] = question_time_vector


# Extract the audio from each .mp4 video and save it as a .wav file
for i in range(len(mp4_filepaths)):
    system('ffmpeg -i {} -vn {}'.format(mp4_filepaths[i], wav_filepaths[i]))

# Iterate through each combination of clip lengths & clip periods
for clip_length in CLIP_LENGTHS:
    for clip_period in CLIP_PERIODS:
        question_truth_labels = {}

        # Create a folder for the group of .wav files corresponding to that clip length & clip period, if it doesn't exist
        split_audio_dir = join(PATH_TO_SPLIT_AUDIO, SPLIT_AUDIO_DIR_CONVENTION.format(clip_length, clip_period))
        if not exists(split_audio_dir):
            makedirs(split_audio_dir)

        # Split each of the main .wav files into rolling windows of clip_length, every clip_period
        for i in range(len(wav_files)):
            # Get the full audio .wav file
            full_audio = AudioSegment.from_wav(wav_filepaths[i])
            question_time_vector = question_times[wav_files[i]]
            
            t1 = 0
            while t1 < len(full_audio):
                t2 = t1 + clip_length

                data_point_dir = join(split_audio_dir, DATA_POINT_DIR_CONVENTION.format(t1, wav_files[i].replace('.wav', '')))
                makedirs(data_point_dir)

                full_clip_filename = join(data_point_dir, SPLIT_AUDIO_FILE_CONVENTION.format(0))
                last_500_filename = join(data_point_dir, SPLIT_AUDIO_FILE_CONVENTION.format(500)) 
                last_200_filename = join(data_point_dir, SPLIT_AUDIO_FILE_CONVENTION.format(200)) 

                full_clip = full_audio[t1:t2]
                
                t_500 = t2 - 500
                t_500 = t_500 if t_500 > t1 else t1
                
                t_200 = t2 - 200
                t_200 = t_200 if t_200 > t1 else t1

                full_clip.export(full_clip_filename, format=WAV_FORMAT)
                full_clip[t_500:t2].export(last_500_filename, format=WAV_FORMAT)
                full_clip[t_200:t2].export(last_200_filename, format=WAV_FORMAT)

                question_truth_labels[data_point_dir] = False
                for time in question_time_vector:
                    if time > t1 and time < t2:
                        question_truth_labels[data_point_dir] = True
                        break

                t1 += clip_period
            
        f = open(join(PATH_TO_MTC_DATA, QUESTION_TRUTH_LABELS_CONVENTION.format(clip_length, clip_period)), "wb")
        pickle.dump(question_truth_labels,f)
        f.close()



