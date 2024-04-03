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
  clock_ptr -> set_year(2020);
  printf("Address of clock: %p\n",clock_ptr);
  printf("Value of clocks year %d\n",clock_ptr ->get_year());
  //or
  printf("Value of clocks year %d\n",(*clock_ptr).get_year());

};
int main(){
    //DereferencingPointers();
    MemeberOfPointerOpterator();
    return 0;
}