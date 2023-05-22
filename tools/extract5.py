#!/usr/bin/env python3

#extract.py

import sys
import os
import h5py
import numpy as np
from scipy.io.wavfile import write

SAMPLERATE = 22050

tax_code = sys.argv[1]
filename = sys.argv[2]
print(tax_code)

try:
  os.mkdir(tax_code)
except FileExistsError:
  print('Directory already exists')

with h5py.File(filename, 'r') as f:
  keys = f['waveforms'].keys()
  counter = 0
  for k in keys:
    dataset = f['waveforms'][k]
    data = dataset[:]
#    counter += 1
#    wav_name = tax_code + '/' + 'clip' + str(counter) + '.wav'
    wav_name = tax_code + '/' + k + '.wav' 
    write(wav_name, SAMPLERATE, data)
  f.close()
