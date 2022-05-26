# .nmf Pattern File Format

For use in our project, we designed a .nmf binary file format in order to store our pattern matrices and other important data. By doing this, we eliminated the need to run NMF everytime we wanted to run a test. This format is as follows:

### Header
The .nmf file format contatins a 16-byte header, which contains the following information:

- "NMFP" - 4-byte signature
- version - 1 byte
- bytes per entry - 1 byte
- number of patterns - u16
- height - u16
- width - u16
- species code - 4 bytes

After the header, the file contains the matrix of patterns, which is stored as a 2D array of floats.