#include <cstdio>
#include <string> // Add the missing string header

int printMessage(int times, const std::string& Message){ // Change the parameter name to avoid redeclaration
    for(int i = 0; i < times; i++) // Change the loop variable name to avoid redeclaration
        printf("%s\n", Message.c_str()); // Use c_str() to print the string
    return 0;//returns 0 defaut escape code for success
}


//create a a custom object or array of objects


int main(){
    printMessage(200,"message");

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
