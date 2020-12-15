# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 12:36:09 2020

@author: uncle
"""

import numpy as np
import scipy as sp

#np.mean()
#np.median()
#np.max()
#np.min()
#np.std() #standard dev
#np.ptp() #range
#sp.stats.kurtosis() #kurtosis, no function in numpy
#sp.stats.skew() #skewness

def get_stats(quantity_vector, sample_rate):
    mean = np.mean(quantity_vector)
    std_dev = np.std(quantity_vector)
    median = np.median(quantity_vector)
    maximum = np.max(quantity_vector)
    minimum = np.min(quantity_vector)
    range_v = np.ptp(quantity_vector)
    skew = sp.stats.skew(quantity_vector)
    kurtosis = sp.stats.kurtosis(quantity_vector)

    all_pts_reg_slope, all_pts_reg_offset, all_pts_reg_mse = all_points_regression(quantity_vector, sample_rate)
    first_last_reg_slope, first_last_reg_offset = first_last_fit(quantity_vector, sample_rate)
    first_last_reg_mse = first_last_MSE(quantity_vector)

    perc_rise_slopes = percent_rising_slopes(quantity_vector)

    return [mean, std_dev, median, maximum, minimum, range_v, skew, kurtosis, all_pts_reg_slope, all_pts_reg_offset, all_pts_reg_mse[0], first_last_reg_slope, first_last_reg_offset, first_last_reg_mse, perc_rise_slopes]

def get_pause_stats(pause_durations, pause_starts):
    mean = np.mean(pause_durations)
    std_dev = np.std(pause_durations)
    median = np.median(pause_durations)
    maximum = np.max(pause_durations)
    minimum = np.min(pause_durations)
    range_v = np.ptp(pause_durations)
    skew = sp.stats.skew(pause_durations)
    kurtosis = sp.stats.kurtosis(pause_durations)

    if (len(pause_durations) > 1):
        fit, SSR, _, _, _= np.polyfit(pause_starts, pause_durations, 1, full=True) #returns the coeefficients for a first degree polynomial, the Sum of squared residuals and some other stuff.
        all_pts_reg_slope, all_pts_reg_offset, all_pts_reg_mse = fit[0], fit[1], SSR/len(pause_durations)
        all_pts_reg_mse = [0] if not all_pts_reg_mse else all_pts_reg_mse
    else:
        all_pts_reg_slope = 0
        all_pts_reg_offset = 5.0
        all_pts_reg_mse = [0]

    return [mean, std_dev, median, maximum, minimum, range_v, skew, kurtosis, all_pts_reg_slope, all_pts_reg_offset, all_pts_reg_mse[0]]

def all_points_regression(vector,sample_rate): #returns the slope, the offset and the MSE of the vector
    t=np.linspace(0,(len(vector)-1)/sample_rate,len(vector)) #time goes from 0 to t final with len(vector) time steps
    fit, SSR, _, _, _=np.polyfit(t,vector,1,full=True) #returns the coeefficients for a first degree polynomial, the Sum of squared residuals and some other stuff.
    return fit[0], fit[1], SSR/len(vector) #returns the slope, the offset, and the MSE where MSE=SSR(Sum of squared residuals)/N

def first_last_fit(vector,sample_rate): #returns the slope and the offset of the first and last point of the vector
    dt=(len(vector)-1)/sample_rate
    return (vector[-1]-vector[0])/dt, vector[0] #returns the slope and the offset

def percent_rising_slopes(vector): #returns the percent of rising slopes as the vector steps forward in time
    n=0 #number of rising slopes
    for i in range(len(vector)-1):
        if vector[i]<vector[i+1]:
            n += 1
    return n/(len(vector)-1) #percent of rising slopes

def first_last_MSE(vector):
    fit_line=np.linspace(vector[0],vector[-1],len(vector))
    MSE=np.mean((fit_line-vector)**2)
    return MSE