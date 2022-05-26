# MAFR.py -- Python module for MAFR

MAFR is a Python module that containss the functions necessary for the project to run smoothly. In most of our source code, you can see that MAFR is imported in nearly every file. MAFR depends on the numpy and PIL modules. Below, you will find explanations of the functions found in MAFR.py

### loadImage(filename, size)

loadImage is a function that takes a path to an image and returns a PIL image object. loadImage also takes in a blockSize and crops the image down to fit the blockSize.

*Parameters:*
 - filename: The path to the image you want to load.
 - size: The size of the block you want to crop the image to.

 *Returns:*
 - A PIL image object.

 ### imageToMatrix(image, size)

 imageToMatrix takes in a PIL image object, and a blockSize. It creates tiles of blockSize x blockSize from the image, and returns a 2d numpy array of the tiles.

*Parameters:*
- image: A PIL image object.
- size: The size of the tiles you want to create.

 *Returns:*
 - A 2d numpy array of the tiles.

 ### matrixToImage(tiles, width, height)

 matrixToImage takes in a 2d numpy array of tiles, a width and a height. It creates a PIL image object of size width x height from the tiles, and returns the PIL image object.

 *Parameters:*
- tiles: A 2d numpy array of tiles.
- width: The width of the image you want to create.
- height: The height of the image you want to create.

*Returns:*
- A PIL image object

### mergeChars(a,b)

mergeChars takes in two characters, combines them, and returns the combined character. This is used in saveMatrix to combine the 4 digit species code into 2 bytes.

*Parameters:*
- a: The first character.
- b: The second character.

*Returns:*
- The combined character.

### saveMatrix(matrix, patterns, block_size, species_code, out=os.getcwd())

saveMatrix takes in a 2d numpy array of patterns, a block size, and a species code. It saves the patterns in .nmf format to the output directory. (see *format.md* for more information on .nmf format)

*Paramaters*
- matrix: A 2d numpy array of patterns.
- patterns: The number of patterns that were kept.
- block_size: The size of the block that was used to create the patterns.
- species_code: The species code of the bird.
- out: The output directory. (optional, defaults to the current working directory)

*Returns:*
- None, but saves the .nmf file to the output directory.

### loadMatrix(mat_file)

loadMatrix takes in a path to a .nmf file and returns a 2d numpy array of the patterns.

*Parameters:*
- mat_file: The path to the .nmf file.
    
*Returns:*
- A 2d numpy array of the patterns.

### computeError(original, patterns)

computeError computes the error between the original matrix and the result of reconstruction from the patterns. It take in two 2d numpy arrays, one representing the original image, and the other representing the patterns that were extracted. Returns the estimated error as a float.

*Parameters*
- original: The original image, as a matrix.
- patterns: The patterns extracted from the original image.

*Returns:*
- The estimated error, as a float.

### getSpecies(mat_file)
getSpecies takes in a .nmf file and returns the species code.

*Parameters:*
- mat_file: The path to the matrix file.

*Returns:*
- The species code.

### getBlockSize(mat_file)

getBlockSize takes in a .nmf file and returns the block size.

*Parameters:*
- mat_file: The path to the matrix file.

*Returns:*
- The block size.

### closestDivisoe(n)

closestDivisor finds the largest divisor of n that is less than sqrt(n).

*Parameters:*
- n: The number you want to find the closest divisor of.

*Returns:*
- The closest divisor of n, less than the sqrt(n).