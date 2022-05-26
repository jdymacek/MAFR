# Magnificent Frigatebird - Nocturnal Flight Call Identification and Classification

MAFR is a series of tools for identifying and classifying nocturnal flight calls. Currently, our tools are written mostly in Python, with one tool written as a web application in HTML and JavaScript. Below, you will find a short explanation of each tool, and how to use it.

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

### lines.html and blocKPicker.js

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

