Workflow.txt -- explains the process of the programs identifying and classifying potential NFCs

If the user is starting over from scratch, they would first have to extract the .wav files from the .h5 files:

1. extract5.py does this by taking in a .h5 file, extarcting the .wav files, and storing those files in a
seperate directory labeled by their taxonomy code.

EXAMPLE: python3 extract5.py BirdVox-14SD_1-4-1_original.h5


The next program will take these audio files and convert them to image files, with the audio files represented
as spectrograms:

2. wavToPng.py takes in a directory of .wav files and returns the spectrogram of that file in the same directory.
This program utilizes Sound eXchange(SoX), a sound processing program, to do this.

EXAMPLE: python3 wavToPng.py -d wavDirectory

To make the signal stronger and the noise less prevelant, we applied multiple filtering methods.
3. simpleFilter.py takes in a directory of wav files and reduces the noise on every file. After the noise
reduction, the new images are stored in a new directory labeled "reducedNoise".
4. blur
5.average
6?. crop



