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

//references are declared by appending the type with the (&) declarator
//much safer than pointers because they cannot be null and they cannot be reassigned (shouldnt generally be assigned to nullptr)
//can be used exactly like the variable they reference so no need for dereferencing or member-of-pointer operator

void add_year(ClockOfTheLongNow& clock){
    clock.set_year(clock.get_year()+1);// no deref operator needed
    }

int main(){
    ClockOfTheLongNow clock;
    printf("Year: %d\n",clock.get_year());
    add_year(clock); // clock os implicitly passed by reference!
    printf("Year: %d\n",clock.get_year());
}
