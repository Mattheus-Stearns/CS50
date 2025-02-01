#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Calculate the average of the RGB values
            int average = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            
            // Assign the average value to each color component
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{

    // doesnt work locally...

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            // Swap the pixels horizontally
            RGBTRIPLE temp = image[i][width - 1 - j];
            image[i][width - 1 - j] = image[i][j];
            image[i][j] = temp;
        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{

    // doesn't work locally

    // Create a temporary image to store the blurred values
    RGBTRIPLE temp[height][width];

    // Iterate over each pixel in the image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sumRed = 0, sumGreen = 0, sumBlue = 0;
            int count = 0;

            // Iterate over the 3x3 grid surrounding the pixel
            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    int ni = i + di;
                    int nj = j + dj;

                    // Check if the neighboring pixel is within the image bounds
                    if (ni >= 0 && ni < height && nj >= 0 && nj < width)
                    {
                        sumRed += image[ni][nj].rgbtRed;
                        sumGreen += image[ni][nj].rgbtGreen;
                        sumBlue += image[ni][nj].rgbtBlue;
                        count++;
                    }
                }
            }

            // Calculate the average color values
            temp[i][j].rgbtRed = round(sumRed / (float)count);
            temp[i][j].rgbtGreen = round(sumGreen / (float)count);
            temp[i][j].rgbtBlue = round(sumBlue / (float)count);
        }
    }

    // Copy the blurred values back to the original image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp[i][j];
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // doesnt work locally

    // Create a temporary image to store the edge-detected values
    RGBTRIPLE temp[height][width];

    // Define Sobel operator kernels
    int Gx[3][3] = {
        {-1, 0, 1},
        {-2, 0, 2},
        {-1, 0, 1}
    };

    int Gy[3][3] = {
        {-1, -2, -1},
        {0, 0, 0},
        {1, 2, 1}
    };

    // Iterate over each pixel in the image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sumRedX = 0, sumGreenX = 0, sumBlueX = 0;
            int sumRedY = 0, sumGreenY = 0, sumBlueY = 0;

            // Iterate over the 3x3 grid surrounding the pixel
            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    int ni = i + di;
                    int nj = j + dj;

                    // Check if the neighboring pixel is within the image bounds
                    if (ni >= 0 && ni < height && nj >= 0 && nj < width)
                    {
                        sumRedX += image[ni][nj].rgbtRed * Gx[di + 1][dj + 1];
                        sumGreenX += image[ni][nj].rgbtGreen * Gx[di + 1][dj + 1];
                        sumBlueX += image[ni][nj].rgbtBlue * Gx[di + 1][dj + 1];

                        sumRedY += image[ni][nj].rgbtRed * Gy[di + 1][dj + 1];
                        sumGreenY += image[ni][nj].rgbtGreen * Gy[di + 1][dj + 1];
                        sumBlueY += image[ni][nj].rgbtBlue * Gy[di + 1][dj + 1];
                    }
                }
            }

            // Calculate the magnitude of the gradient
            int red = round(sqrt(sumRedX * sumRedX + sumRedY * sumRedY));
            int green = round(sqrt(sumGreenX * sumGreenX + sumGreenY * sumGreenY));
            int blue = round(sqrt(sumBlueX * sumBlueX + sumBlueY * sumBlueY));

            // Ensure the values are within the valid range [0, 255]
            temp[i][j].rgbtRed = red > 255 ? 255 : red;
            temp[i][j].rgbtGreen = green > 255 ? 255 : green;
            temp[i][j].rgbtBlue = blue > 255 ? 255 : blue;
        }
    }

    // Copy the edge-detected values back to the original image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp[i][j];
        }
    }
    return;
}
