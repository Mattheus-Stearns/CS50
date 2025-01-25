#include <cs50.h> // string get_string(string prompt);
#include <stdio.h> // int printf(string format, ...);

int main() {

    string name = gets_string("What is your name?");
    printf("Hello, %s!\n", name);
}

// clang -o hello hello.c == make hello

// after adding cs50, it becomes: clang -o hello hello.c -lcs50 == make hello
// -> this is because the cs50 library is not in the standard library path, also the -l flag is used to link the library

// -> also, the math library is included in c by default, so we don't need to include it in the command line

// Four different stages: Preprocessing, Compiling, Assembling, Linking

// different types of data in C: int: 4 bytes, float: 4 bytes, double: 8 bytes, char: 1 byte, string: ?, bool: 1 byte