# Workflow.md 
This document explains the process of the programs identifying and classifying potential NFCs


### If the user is starting over from scratch, they would first have to extract the .wav files from the .h5 files:

1. extract5.py does this by taking in a .h5 file, extarcting the .wav files, and storing those files in a seperate directory labeled by their taxonomy code.

`python3 extract5.py <h5 file>`

&nbsp;


### The next program will take these audio files and convert them to image files, with the audio files represented as spectrograms:

2. wavToPng.py takes in a directory of .wav files and returns the spectrogram of that file in the same directory. This program utilizes Sound eXchange(SoX), a sound processing program, to do this.

`python3 wavToPng.py -d <directory of .wav files>`

&nbsp;


### To make the signal stronger and the noise less prevalent, we applied multiple filtering methods.

3. simpleFilter.py takes in a directory of .wav files and reduces the noise on every file. After the noise reduction, the new images are stored in a new directory labeled "reducedFromBoth".

`python3 simpleFilter.py -t <directory of audio files>`

&nbsp;

4. gaussianFilter.py takes in a directory of images and uses gaussian blur on the images. The gaussian blur takes a blur radius, the intensity of the blur, that the user gives and applies it to each image. The blur will help spread out the signal, strengthening the presence of a signal.

`python3 gaussianFilter.py -r <blur radius> -t <directory of images>`

&nbsp;


### The user can create a training and testing set with the audio files. 

5. splitSets.py takes in a directory of audio files and splits it based on the percentage the user provides as a float. The program will create a training and testing directory named after the species the audios belong to. This program orignally used a 60-40 split, but it can be adjusted, though the results may be more accurate if the training set has more than the testing set. 

`python3 splitSets.py <audio file directory> <species name> <custom percent>`

&nbsp;


### Now that the user has their training and testing sets, our training program will use the training set to get the best possible patterns to use for the following classifier.

6. eigenTrain.py takes in the training directory, -t, with the number of patterns desired, -p. It also takes in the number of pixels to be removed from the bottom of the image, -r, so the program will focus on where the actual signal is located. The center width of the signal, -w, should be stated to further focus on where the signal is located. After running through the set, it will return the pattern file. This pattern file contains the number of patterns specified earlier.  

`python3 eigenTrain.py -t <training directory> -p <number of patterns> -r <pixels to be removed from bottom> -w <center width as pixels>`

&nbsp;


### We built a classification Class to organize the different classifiers we have implemented. All of the classifiers take a pattern file with its coefficients file to classfiy all of the files in the testing set.

7. eigenTest.py takes in the testing directory, -d, and a pattern file, -p, with its matching .csv file of coefficients, -w created from the previous trainer. It then uses each classifier in EigenClassifier.py and returns the scores so we can compare how well each classifier did.

- *EigenClassifier*: Classifies each file based on the largest coefficient and its paired species.  

- *EigenMajority*: Finds the top five largest coefficients for each files and checks the species that appears the most in the top five. The species that appears at least two or more times is what that file gets classified as. 

- *EigenAverage*: Looks for the top three coefficients per species for each file and takes the average. The species that has the lowest average is the species the file gets classified as. 

`python3 eigenTest.py -p <patternFile> -d <testing directory> -w <coefficient file as a .csv>`

&nbsp;


