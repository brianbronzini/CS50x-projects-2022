#include <stdio.h>
#include <stdlib.h>
#include<stdint.h>
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // check that argument count is 2
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // open file
    FILE *input_file = fopen(argv[1], "r");

    // check that input_file is valid
    if (input_file == NULL)
    {
        printf("The file could not be opened");
        return 2;
    }

    // store blocks of 512 bytes in array
    unsigned char buffer[512];

    // track generated images
    int count_image = 0;

    // file pointer for recovered images
    FILE *output_file = NULL;

    // char filename[8]
    char *filename = malloc(8 * sizeof(char));

    // read over the blocks of 512 bytes
    while (fread(buffer, sizeof(char), 512, input_file))
    {
        // check bytes determine start of the JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // write the filesnames for JPEG
            sprintf(filename, "%03i.jpg", count_image);

            // open output_file to write
            output_file = fopen(filename, "w");

            // count number of images
            count_image++;
        }
        // check if output contains valid input
        if (output_file != NULL)
        {
            fwrite(buffer, sizeof(char), 512, output_file);
        }
    }
    // close files and free memory from previous allocation (malloc)
    free(filename);
    fclose(input_file);
    fclose(output_file);

    return 0;
}