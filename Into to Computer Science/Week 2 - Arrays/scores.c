#include <stdio.h>
#include <cs50.h>

const int N = 3;

float average(int length, int array[]);

int main(void) {
    // int score1 = 72;
    // int score2 = 73;
    // int score3 = 33;

    int scores[N];

    // scores[0] = 72;
    // scores[1] = 73;
    // scores[2] = 33;

    for (int i = 0; i < N; i++) {
        scores[i] = get_int("Score: ");
    }

    // Average
    printf("Average: %f\n", average(N, scores));
}

float average(int length, int array[]) {
    int sum = 0;
    for (int i = 0; i < length; i++) {
        sum += array[i];
    }
    return sum / (float) length;
}