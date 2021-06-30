#include <stdio.h>
#include <unistd.h> 

int main()
{
    int p[2];
    pipe(p);
    FILE *emulated_file = fdopen(p[0], "r");
    write(p[1], "whatevereyouwant", 17);

    char buf[32];
    fread(&buf, 1, 32, emulated_file);
    printf("%s\n", buf);
    return 0;
}