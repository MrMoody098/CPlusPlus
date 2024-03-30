#include <cstdio>

void taunt(){
    printf("Your mother was a hamster and your father smelt of elderberries!\n");
}

int my_array[100]; // Declare an array of 100 integers

int array[] = {1,2,3,4,5}; // Declare an array of 5 integers and initialize it

//Accessing arrays
int main(){
    int arr[] = {1,2,3,4};
    printf("third element is %d\n",arr[2]); // Prints 1
    arr[2] = 100;
    printf("third element is %d\n",arr[2]); // Prints 100

    unsigned long maximum = 0;
    unsigned long values[] = {10, 50, 20, 40, 30};
    for(unsigned long value: values){
        if(value > maximum){
            maximum = value;
        }
    }
    printf("The maximum value is %lu\n", maximum);

    char alphebet[27];
    for (int i = 0;i<26;i++){
        alphebet[i] =i+97;
        printf("%c\n",alphebet[i]);
    }
size_t n_elements = sizeof(alphebet) / sizeof(alphebet[0]);//size of array = size of array bites / size of first element in bites

printf("The array has %zu elements\n",n_elements);
}