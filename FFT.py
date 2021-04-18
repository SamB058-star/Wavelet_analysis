# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 21:11:02 2021

@author: SAM
"""

import numpy as np
import pandas as pd
import os, glob
import matplotlib.pyplot as plt
import scipy as sp
import scipy.fftpack
import scipy.stats

file_path = r'D:\DATA C\Desktop\Stations_data\Bansathi\Bansathi_all_months_copy'
# file_path = r'D:\DATA C\Desktop\Stations_data\Bani\all_months_copy'
os.chdir(file_path)

# df = pd.read_csv('08_October_2020.csv', sep = ',')
df = pd.read_csv('08_Bans_October_2020.csv', sep = ',') #arse_dates = 'date')

df['date'] = pd.to_datetime(df.date, format = '%d.%m.%Y %H:%M:%S')
df.set_index('date', inplace = True)
df_1hr = df.resample('60min').mean()
df_1day = df.resample('1440min').mean()
print(df)

date_mask = (df_1hr.index > '2020-10-01') & (df_1hr.index <= '2020-10-31')
date_mask2 = (df_1day.index > '2020-10-01') & (df_1day.index <= '2020-10-31')

# Moisture Data
SM_sensor1 = df_1hr['S1SM'].loc[date_mask]
SM_day_S1 = df_1day['S1SM'].loc[date_mask2]
# Temperature data
ST_sensor1 = df_1hr['S1Temp'].loc[date_mask]
ST_day_S1 = df_1day['S1Temp'].loc[date_mask2]
# plt.plot(df.index, df.S1SM)

plt.plot(SM_sensor1.index, SM_sensor1.values, ':')
plt.xticks(rotation = 35)
# SoilMoi = df.S1SM.values
# n = df.index.size
# # print(SoilMoisture)
# period = 24
# print(period)
## 1 Day frequency
date = SM_sensor1.index
soilmoisture = SM_sensor1.values

soiltemp = ST_sensor1.values

N = 7*24 #len(date)/len(SM_day_S1)
print(N)

#you have to adjust timing here:
soilmoisture_fft = sp.fftpack.fft(soilmoisture)
soilmoisture_psd = np.abs(soilmoisture_fft)**2
fftfreq = sp.fftpack.fftfreq(len(soilmoisture_psd), 1/N)

##  FFT of Temperature
soiltemp_fft = sp.fftpack.fft(soiltemp)
soiltemp_psd = np.abs(soiltemp_fft)**2
fftfreq = sp.fftpack.fftfreq(len(soilmoisture_psd), 1/N)

i = fftfreq > 0
fig, ax = plt.subplots(1, 1, figsize=(8, 4), dpi = 300)
ax.plot(fftfreq[i], 10 * np.log10(soilmoisture_psd[i]), 'r-',
        label = 'Soil Moisture Specturm')
ax.plot(fftfreq[i], 10 * np.log10(soiltemp_psd[i]), 'g--',
        label = 'Soil Temperature Specturm')
# ax.set_xlim(0, 2)
ax.set_xlabel('Frequency (1/day)')
ax.set_ylabel('PSD (dB)')
ax.legend()
ax.set_title('Frequency Spectrums of Bansathi')
plt.grid()
plt.show()
# print(soilmoisture_fft)

# first_peak_mask = [(np.abs(soilmoisture_fft) < 10)]
                   #& (np.abs(soilmoisture_fft) > 4)]

# mask = [((fftfreq) < 6)  & ((fftfreq) > 8)]
soilmoi = soilmoisture_fft.copy()
soilmoi[((fftfreq) > 20)] = 0
first_waveform = sp.fftpack.ifft(soilmoi)

soitemp = soiltemp_fft.copy()
# soiltemp[np.abs(fftfreq) > 1.5] = 0
soitemp[((fftfreq) > 20)] = 0
temp_waveform = sp.fftpack.ifft(soitemp)

## Plots after filtering
fig, ax1 = plt.subplots(3,1, figsize=(12, 10), dpi = 600)
ax1[0].plot(fftfreq[i], soilmoi[i], 'g', label = 'SM Filtered spectrum')
ax1[0].plot(fftfreq[i], soitemp[i], 'r--', label = 'ST Filtered spectrum')
ax1[0].set_xlabel('Frequency (1/day)')
ax1[1].plot(date, first_waveform, 'm', label = 'SM Filtered waveform')
ax1[1].plot(date, soilmoisture, 'k--', label = 'Original SM')
ax1[1].set_xlabel('Date')
ax1[2].plot(date, temp_waveform, 'b', label = 'ST Filtered waveform')
ax1[2].plot(date, soiltemp, 'r--', label = 'Original ST')
ax1[2].set_xlabel('Date')
ax1[0].legend()
ax1[1].legend()
ax1[2].legend()
# ax1[1].plot(date, temp_waveform, 'k')
fig, ax3 = plt.subplots(figsize = (10, 5), dpi = 500)
# plt.figure(figsize = (12, 5), dpi = 500)
ax3.plot(date, first_waveform, 'r:', label = 'SM')
ax3.plot(date, temp_waveform, 'b:', label = 'ST')
plt.xticks(rotation = 35)
ax3.legend()

## Correlation analysis
# correlation, _ = scipy.stats.kendalltau(first_waveform, temp_waveform)
# print('Correlation: %.3f' % correlation)
# print(_)

print(first_waveform.corr(temp_waveform))

fig, ax4 = plt.subplots(figsize = (6, 5), dpi = 500)
ax4.scatter(first_waveform, temp_waveform)
# ax4.legend()

# # second_pick = [(fftfreq > 1.8) & (fftfreq <= 2.2)]
# # speak_freq = freqs[soilmoisture_psd[i][second_pick]]
# #  Filtering
# freqs = fftfreq[i]
# peak_freq = freqs[soilmoisture_psd[i].argmin()]
# print(peak_freq)


# ## 1 hour frequency
# date = SM_sensor1.index
# soilmoisture = SM_sensor1.values
# N2 = len(date)
# print(N)

# #you have to adjust timing here:
# soilmoisture_fft = sp.fftpack.fft(soilmoisture)
# soilmoisture_psd = np.abs(soilmoisture_fft)**2
# fftfreq = sp.fftpack.fftfreq(len(soilmoisture_psd), 1/N2)
# i = fftfreq > 0
# fig, ax = plt.subplots(1, 1, figsize=(8, 4))
# ax.bar(fftfreq[i], 10 * np.log10(soilmoisture_psd[i]), bins = 1000)
# # ax.set_xlim(1.5, 3)
# ax.set_xlabel('Frequency (1/day)')
# ax.set_ylabel('PSD (dB)')
# # print(soilmoisture_fft)

# second_pick = [(fftfreq > 1.8) & (fftfreq <= 2.2)]
# #  Filtering
# # peak_freq = freqs[power[pos_mask].argmax()]