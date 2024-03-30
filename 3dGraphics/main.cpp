#include "screen.h"

int main()
{
    

    #Screen screen;
    for(int i = 0; i < 100; i++)
    {
        screen.pixel(rand()%640,rand()%480);
    }


    while(1)
    {
        screen.show();
        screen.input();
    }
    
    return 0;


}