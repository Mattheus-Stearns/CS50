#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    while (argc != 2)
    {
        printf("Correct implementation: ./recover data\n");
        return 1;
    }

    FILE *data = fopen(argv[1], "r");
    if (data == NULL)
    {
        printf("File not found\n");
        return 1;
    }

    unsigned char buffer[512];
    int count = 0;
    FILE *img = NULL;
    char filename[8];
    while (fread(buffer, 512, 1, data) == 1)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (count > 0)
            {
                fclose(img);
            }
            sprintf(filename, "%03i.jpg", count);
            img = fopen(filename, "w");
            count++;
        }
        if (count > 0)
        {
            fwrite(buffer, 512, 1, img);
        }
    }

    fclose(data);
    fclose(img);

    return 0;
    
}
