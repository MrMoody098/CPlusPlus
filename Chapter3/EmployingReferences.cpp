#include <cstdio>
//pointers provide a lot of flexibility, but this comes at a saftey cost.

//if you dont need the flexibility of reseatability(being able to reasign a pointer) 
//and nullptr references are the go-to reference type

//to drive home the point that references cant be seated this example intialises an 
//int reference and then attempts to reseat it with a new_value

int main(){
    int orignal =100;
    int& orignal_ref = orignal;
    printf("Orignal: %d\n",orignal);
    printf("Refernce: %d\n",orignal_ref);

    int new_value = 50;
    orignal_ref = new_value; //we set orignal_ref to new_value if it was a pointer we would be changing the pointer value and not the value its pointing to
    printf("Orignal: %d\n",orignal); //because it is a refernce it changes the pointed to object rather than the reference
    printf("New Value: %d\n",new_value);//all of these values get changed to 50
    printf("Refernce: %d\n",orignal_ref);//
}