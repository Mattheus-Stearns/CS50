#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    /* MARK: -- OLD WAY
    int list[3];

    list[0] = 1;
    list[1] = 2;
    list[2] = 3;
    
    for (int i = 0; i < 3; i++)
    {
        printf("%i\n", list[i]);
    }
    */

    int *list = malloc(3 * sizeof(int));
    if (list == NULL)
    {
        return 1;
    }

    list[0] = 1;
    list[1] = 2;
    list[2] = 3;

    // Time passes

    int *tmp = realloc(list, 4 * sizeof(int));
    if (tmp == NULL)
    {
        free(list);
        return 2;
    }
    
    tmp[3] = 4;

    free(list);

    list = tmp;

    for (int i = 0; i < 4; i++)
    {
        printf("%i\n", list[i]);
    }

    // Time passes

    free(list);
    return 0;

}