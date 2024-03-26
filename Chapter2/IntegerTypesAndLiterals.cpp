#include <cstdio>

int rileysGay(){
    for(int i = 0; i <10000;i++)printf("Riley is gay\n");
    return 0;
}


//create a a custom object or array of objects


int main(){
    rileysGay();

    bool Condition = false;
    unsigned short a = 0b1010101010;
    printf("%hu\n",a); 
    int b = 0123;
    printf("%d\n",b);
    unsigned long long d = 0xFFFFFFFFFFFFF;
    printf("%llu\n",d);

    unsigned int usInt = 3669732608;
    printf("Yabba %x!\n",usInt);
    unsigned int usInt1 =69;
    printf("There are %u,%o Leaves Here.\n",usInt1,usInt1);//u is the orignal one x is for hex and %o is for octal
    if(Condition) return 0;
    else return 1;
}
