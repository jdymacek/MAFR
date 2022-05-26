# Magnificent Frigatebird - Nocturnal Flight Call Identification and Classification

MAFR is a series of tools for identifying and classifying nocturnal flight calls. Currently, our tools are written mostly in Python, with one tool written as a web application in HTML and JavaScript. Below, you will find a short explanation of each tool, and how to use it.

### MAFR.py

MAFR.py is a Python module that contains the functions necessary for the below tools to function correctly. MAFR uses the numpy and PIL libraries. Please see *MAFR.md* for more information.

### extract5.py

extract5.py is a Python script that extracts the waveform data from the .h5 files from the Birdvox-14SD dataset. Usage is as follows:

    `python3 extract5.py <.h5 filename>`

    <.h5 filename> is the name of the .h5 file to be processed.

### scrape.py

scrape.py is a Python web scraper that scraped the Birdvox-14SD dataset. It is written in Python and uses the requests and BeautifulSoup libraries. Usage is as follows:

    `python3 scrape.py`

### splitSets.py

splitSets.py is a Python script that splits the Birdvox-14SD dataset into training and test sets. Usage is as follows:

    `python3 splitSets.py <directory of files to split> <output directory> <training set percentage>`

    <directory of files to split> is the directory containing the .png files to be split.
    <output directory> is the directory to which the split files will be written.
    <training set percentage> is the percentage of files to be written to the training set.

### wavToPng.py
    
wavToPng.py is a Python script that converts .wav files to .png files. Usage is as follows:
    
    `python3 wavToPng.py <directory of .wav files>`
    
    <directory of .wav files> is the directory containing the .wav files to be converted.

### extractBlocks.py

extractBlocks.py is a Python script that extracts selected blocks from the training set. extractBlocks uses the PIL and numpy libraries and usage is as follows:

    `python3 extractBlocks.py <directory of .png files> <.txt file with annotations>'
            
    <directory of .png files> is the directory containing the .png files to be processed.
    <.txt file with annotations> is the .txt file that contains the desired blocks.

### lines.html and blockPicker.js

lines.html and blockPicker.js make up a web application that allows the user to select blocks from each file in the training set. To use the application, you load in your dataset into the blockPicker.js 'files' array, and then open the lines.html file in your browser. Once there, you can select blocks by clicking on the image, which will populate the file's name and the selected blocks into the text area. You can copy the text area to the clipboard, and then paste it into a textfile to save your annotations.

### patternMaker.py

patternMaker.py is a Python script that generates .nmf pattern files from images using non-negative matrix factorization. patternMaker uses the numpy, PIL, and sklearn libraries and Usage is as follows:

        `python3 patternMaker.py -d <input-directory> -p <patterns> -b <blockSize> -o <output-directory> -s <species-code> -n <image-number>'

        input-directory: directory of .png files to generate patterns
        patterns: how many patterns to keep in each .nmf file
        blockSize: size of each pattern
        output-directory: directory to write .nmf files out to
        species-code: species code of imcoming data
        image-number: number of images to use in each pattern file

### autoPattern.py

autoPattern.py is a Python script that generates .nmf pattern files from images using non-negative matrix factorization, similar to patternMaker.py. However, autoPattern will run on an entire directory of directories, significantly streamlining the process. autoPattern uses the numpy, PIL, and sklearn libraries and Usage is as follows:

        `python3 autoPattern.py -d <input-directory> -p <patterns> -b <blockSize> -o <output-directory> -s <patterns per species> -n <image-number>'

        input-directory: directory of .png files to generate patterns
        patterns: how many patterns to keep in each .nmf file
        blockSize: size of each pattern
        output-directory: directory to write .nmf files out to
        patterns per species: how many patterns to keep per species
        image-number: number of images to use in each pattern file

### naiveclassifier.py

naiveclassifier.py was our first attempt at NFC classification. This classifier computes estimated reconstruction error of each pattern file against a given image. Usage is given below:

    `python3 naiveclassifier.py -d <directory of .nmf pattern files> -f <image file to test> -b <block-size>`

    <directory of .nmf pattern files> is the directory containing the .nmf pattern files to be tested.
    <image file to test> is the image to be tested against the .nmf pattern files.
    <block-size> is the size of each block in the pattern file.

### naiveDir.py

naiveDir is a wrapper for the above naiveclassifier that can run on an entire testing set of images. After completion, naiveDir places all results in a .txt file written to the specified output directory. Usage is as follows:

    `python3 naiveDir.py -d <directory of .nmf pattern files> -i <directory of image files to test> -b <block-size> -o <output-directory>`

    <directory of .nmf pattern files> is the directory containing the .nmf pattern files to be tested.
    <directory of image files to test> is the directory containing the image files to be tested.
    <block-size> is the size of each block in the pattern file.
    <output-directory> is the directory to write the output files to.

### tournamentclassifier.py

tournamentclassifier.py is a classifier that, like naiveclassifier, computes the reconstruction error of each pattern file against a given image. However, to determine a winner, two random pattern files are selected and the pattern with the lowest reconstruction error is selected as the winner. We do 10,000 rounds of this. Usage is as follows:

    `python3 tournamentclassifier.py -d <directory of .nmf pattern files> -f <image file to test> -b <block-size>`

    <directory of .nmf pattern files> is the directory containing the .nmf pattern files to be tested.
    <image file to test> is the image to be tested against the .nmf pattern files.
    <block-size> is the size of each block in the pattern file.