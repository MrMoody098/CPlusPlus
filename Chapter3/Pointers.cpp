#include <cstdio>
 
struct ClockOfTheLongNow {
    ClockOfTheLongNow() {
        year = 2021;
    }
    void add_year() {
        year++;
    }
    void set_year(int new_year) {
        year = new_year;
    }
    int get_year() {
        return year;
    }
    int year;
};

struct College{
        char name[256];
};

void pointinTo(){
    int my_int = 42;
    int* my_pointer = &my_int;
    printf("my_int is %d\n",my_int);
    printf("my_pointer is %p\n",my_pointer);
    printf("the value of my_pointer is %d\n",*my_pointer);
}

void AddressingVariables(){
    //declare a pointers type by appending an asterisk to the pointed-to type
    int* my_pointer; // Declare a pointer to an integer

    //format specifier for pointers is %p
    printf("the value of mn_pointer is %p\n",my_pointer);


    //you can obtain the address of variable by appending the address-of opterator (&)
    int my_int{};
    printf("my_int is %d\n",my_int);
    int *my_int_address = &my_int;
    printf("myy0_int_address is %p\n",my_int_address);

    int gettysburg{};
    printf("gettysburg: %d\n",gettysburg);
    int* gettysburg_address = &gettysburg;
    printf("gettysburg_address: %p\n",gettysburg_address);
    printf("sizeof(gettysburg) : %zu\n",sizeof(gettysburg));
};
void DereferencingPointers(){
    //dereference a pointer by prepending the pointer with an asterisk(*)
    //it is the oppodite of the address-of operator (&)
    
    int gettysburg{};
    int* gettysburg_address = &gettysburg;
    printf("value of gettysburg_address : %d\n",*gettysburg_address);
    printf("gettysburg_address:%p\n", gettysburg_address);
    *gettysburg_address = 17325;
    printf("gettysburg value : %d\n",*gettysburg_address);
    printf("gettysburg_address : %p\n",gettysburg_address);
};

void MemeberOfPointerOpterator(){
//the member of operator or arrow operator(->) performs two operations simultaneously:
//  it derefences a pointer
//  it  accesses a member of pointed-to object.

   

  ClockOfTheLongNow clock;
  ClockOfTheLongNow* clock_ptr = &clock;
  clock_ptr -> set_year(2020); //equivalent to (*clock_ptr).set_year(2020)
  printf("Address of clock: %p\n",clock_ptr);
  printf("Value of clocks year %d\n",clock_ptr ->get_year());
  //or
  printf("Value of clocks year %d\n",(*clock_ptr).get_year());

};

void PointersAndArrays(){
    //pointers and arrays are closely related in C++ 

    //When you define an array in C++, the array's name can be used as a pointer to the first element of the array. 
    //This is because the array's name is essentially a constant pointer to the first element.

    int key_to_the_universe[] = {3, 6, 9};
    int* key_ptr = key_to_the_universe; //points to the first element of the array which is 3 
   
    College best_colleges[] = {"Magdalen","Nuffield","Kellogg"};
    College* college_ptr = best_colleges;
    printf("College name: %s\n",college_ptr -> name);
    

    
};
        //Function For HandlingDecay

    void printNames(College* colleges,size_t n_colleges){
            for (size_t i = 0;i< n_colleges;i++){
                printf("%s College\n",colleges[i].name);
            }
    };

void HandlingDecay(){
    College oxford[] = {"Magdalen","Nuffield","kellog"};
    printNames(oxford,sizeof(oxford)/sizeof(College));
};

void PointerArithemtic(){
    College oxford[] = {"Magdalen","Nuffield","kellog"};

    College* third_college_ptr = &oxford[2];
    
    College* third_College_ptr = oxford + 2;
};

void BufferOverflows(){
    //for arrays and pointers,you can access arbitaty array elements with the bracket opetator ([]) or with pointer arithmetic.
    char lower[] = "abc?e";
    char upper[] = "ABC?e";
    char* upper_ptr = upper; //equivelent to &upper[0]

    lower[3] = 'd'; //lower now contains a b c d e \0
    upper[3] = 'D'; //upper now contains A B C D E \0

    char letter_d = lower[3]; //letter_d is now 'd'
    char letter_D = upper_ptr[3]; //letter_D is now 'D'

    printf("lower: %s\nupper: %s\n",lower,upper);

    //lower[7] = 'g'; //Buffer overflow super BAD we are writing to memory that does not belong to us 
};

int main(){
    //DereferencingPointers();
    //MemeberOfPointerOpterator();
    //PointersAndArrays();
    //HanddlingDecay();
    BufferOverflows();
    //PointerArithemtic();

    return 0;
}