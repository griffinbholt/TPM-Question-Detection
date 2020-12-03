# -*- coding: utf-8 -*-
"""
Created on Tues Nov 24 15:46:29 2020

@author: tysum
"""

import parselmouth
import matplotlib.pyplot as plt
import numpy as np

# functions
def calculate_fundemental_frequency(soundObj):
    pitchObj = soundObj.to_pitch()
    F0 = pitchObj.selected_array['frequency']
    F0[F0==0] = np.nan # if no info give nan rather than 0
    stdevF0 = parselmouth.praat.call(pitchObj, "Get standard deviation", 0 ,0, "Hertz") # zeros indicate full range
    time_vector = pitchObj.xs()
    return F0, stdevF0, time_vector

def calculate_signal_intensity(soundObj):
    intensityObj = soundObj.to_intensity()
    timeVector = intensityObj.xs() # does
    intensityValues = intensityObj.values.T
    return intensityValues, timeVector

def calculate_MFCC_coefficients(soundObj, numCoefficients):
    MFCCobj = sClip.to_mfcc(numCoefficients)
    mfccs = MFCCobj.to_array()
    startTime = MFCCobj.x1
    finalTime = MFCCobj.nx*MFCCobj.dx + startTime
    timeVector = np.arange(startTime, finalTime, MFCCobj.dx)
    return mfccs, timeVector # always gives n+1 coefficents c0 to cn max praat calculates is n = 19

def calculate_zero_crossing_rate(soundObj):
    f0min = 75.0 # praat default for voice
    f0max = 600.0 # praat default for voice
    PPobj = parselmouth.praat.call(soundObj, "To PointProcess (periodic, cc)", f0min, f0max)
    numCrossings = parselmouth.praat.call(PPobj, "Get number of points")
    timeVector = soundObj.xs()
    timePeriod = timeVector[-1] - timeVector[0]
    return numCrossings/timePeriod # crossings per second

def calculate_jitter_of_audio_clip(soundObj):
    f0min = 75.0 # praat default for voice
    f0max = 600.0 # praat default for voice
    pointProcess = parselmouth.praat.call(soundObj, "To PointProcess (periodic, cc)", f0min, f0max)
    localJitter = parselmouth.praat.call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3) # numbers praat defaults
    #localabsoluteJitter = parselmouth.praat.call(pointProcess, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)
    #rapJitter = parselmouth.praat.call(pointProcess, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
    #ppq5Jitter = parselmouth.praat.call(pointProcess, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)
    #ddpJitter = parselmouth.praat.call(pointProcess, "Get jitter (ddp)", 0, 0, 0.0001, 0.02, 1.3)
    return localJitter # I included all jitter functions because I havn't been able to determine one specific to use

def calculate_shimmer_of_audio_clip(soundObj):
    f0min = 75.0 # praat default for voice
    f0max = 600.0 # praat default for voice
    pointProcess = parselmouth.praat.call(soundObj, "To PointProcess (periodic, cc)", f0min, f0max)
    localShimmer =  parselmouth.praat.call([soundObj, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    #localdbShimmer = parselmouth.praat.call([soundObj, pointProcess], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    #apq3Shimmer = parselmouth.praat.call([soundObj, pointProcess], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    #aqpq5Shimmer = parselmouth.praat.call([soundObj, pointProcess], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    #apq11Shimmer =  parselmouth.praat.call([soundObj, pointProcess], "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    #ddaShimmer = parselmouth.praat.call([soundObj, pointProcess], "Get shimmer (dda)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    return localShimmer # I included all jitter functions because I havn't been able to determine one specific to use


def calculate_number_of_pauses(soundObj):
    return #num_pauses

def calculate_length_of_pauses(soundObj):
    
    return

def calculate_spectral_balance(soundObj):
    specObj = soundObj.to_spectrum();
    lowBand = (0.0, 500.0)
    highBand = (1000.0, 2000.0)
    balance = specObj.get_band_energy_difference(lowBand, highBand)    
    return balance

def calculate_power_spectral_density(soundObj):
    specObj = soundObj.to_spectrogram()
    times = specObj.ts()
    specAtTime = specObj.to_spectrum_slice(times[0])
    frequencies = np.linspace(specAtTime.fmin, specAtTime.fmax, specAtTime.get_number_of_bins())
    numTimes = len(times)
    numFreq = len(frequencies)
    fullPSD = np.empty((numTimes,numFreq-1)) # last frequency always gives nan power
    for i in range(numTimes):
        for j in range(numFreq-1):
            fullPSD[i][j] = specObj.get_power_at(times[i], frequencies[j])
    
    averagePSD = np.mean(fullPSD,axis = 0)
    return averagePSD

def calculate_RMS_frame_energy(soundObj):
    return soundObj.get_root_mean_square()



# testing
sClip = parselmouth.Sound("C:/Users/tysum/School/TPM-Question-Detection/testclip.wav")
#f0, timeVector = calculate_fundemental_frequency(sClip)
#intensity, timeVector2 = calculate_signal_intensity(sClip)
#ZCR = calculate_zero_crossing_rate(sClip)
#calculate_power_spectral_density(sClip)
#shim = calculate_shimmer_of_audio_clip(sClip)
#jit = calculate_jitter_of_audio_clip(sClip)
#bal = calculate_spectral_balance(sClip)
psd = calculate_power_spectral_density(sClip)
rmsfe = calculate_RMS_frame_energy(sClip)
