# Workflow.md 
This document explains the process of the programs identifying and classifying potential NFCs


### If the user is starting over from scratch, they would first have to extract the .wav files from the .h5 files:

1. extract5.py does this by taking in a .h5 file, extarcting the .wav files, and storing those files in a seperate directory labeled by their taxonomy code.

*EXAMPLE*: python3 extract5.py BirdVox-14SD_1-4-1_original.h5




### The next program will take these audio files and convert them to image files, with the audio files represented as spectrograms:

2. wavToPng.py takes in a directory of .wav files and returns the spectrogram of that file in the same directory.
This program utilizes Sound eXchange(SoX), a sound processing program, to do this.

*EXAMPLE*: python3 wavToPng.py -d wavDirectory




### To make the signal stronger and the noise less prevalent, we applied multiple filtering methods.

3. simpleFilter.py takes in a directory of .wav files and reduces the noise on every file. After the noise
reduction, the new images are stored in a new directory labeled "reducedNoise".

*EXAMPLE*: python3 simpleFilter.py -t audioDirectory 

4. blur.py 
5. averageNFC.py takes in a directory of .wav files. It groups the .wav files in twos then takes the average of both, producing a new image from the result and moving it into a new directory.

*EXAMPLE*: python3 averageNFC.py -t wavDirectory



### The user can create a training and testing set with the audio files. 

6. splitSets.py takes in a directory of audio files and splits it based on the percentage the user provides as a float. The program will create a training and testing directory named after the species the audios belong to.

*EXAMPLE*: python3 splitSets.py audioDirectory speciesName customPercent




### Now that the user has their training and testing sets, our training program will use the training set to get the best possible patterns to use for the following classifier.

7. eigenTrain.py takes in the training directory with the number of patterns desired. It also takes in the number of pixels to be removed from the bottom of the image so the program will focus on where the actual signal is located. After running through the set, it will return the pattern file. 

*EXAMPLE:* python3 eigenTrain.py -t trainingDirectory -p 64 -r 96




### For classification, it will use the testing set and the created pattern file from training the training set. 

8. eigenClassify.py takes in the testing directory and a pattern file. It utilizes a confusion matrix to examine the likelihood that the given file is a particular species. Since it keeps tracks of this for every file, it then returns the score of how many files it guessed correctly.

*EXAMPLE*: python3 eigenClassify.py -p patternFile -d testingDirectory




