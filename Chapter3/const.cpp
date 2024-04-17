#include <cstdio>

//const is a safety mechanism that prevents modifications of member variables.
//youll use const in function and class operations to specify that a variable will never be changed
//this can stop alot common programming mistakes at compile time

//lets take a look at some Common uses:

    //const Arguments
//a const pointer or reference provides you with an effective mechanism to pass an object into a function for read-only use

void petruchio(const char* shrew){
    printf("Fear not sweet wench,they shall not touch thee %s",shrew);// we can read from shrew
    //shrew[0] = "K"; // but attempting to write to it causes a Compiler error as we cannot change a const 
};

    //const Methods
//making a method const means that it cannot modify the current objects state within the const method
//i.e it is a read only method

struct ClockOfTheLongNow{
    ClockOfTheLongNow(long int year) : year {year}{}
    int get_year() const { // place const between the arg list and method body 
        return year;// had we atempted to modify year it would return a compiler error
    }
    private:
        long int year;
};

//Holders of const refernces and pointers cannot invoke methods taht are not const as they might try to modify an objects state
bool is_leap_year(const ClockOfTheLongNow& clock){ 
    if(clock.get_year() % 4 > 0) return false; //had get_year() not been marked const this would not compile because 
                                               //clock is a const reference and cannot be modified within is_leap_year
    if(clock.get_year() % 100 > 0) return true;
    if(clock.get_year() % 400 >0) return false;
    return true;
};

    //const Member Variables
//you can mark member variables const by addin the keyword to the memebers type
// struct Avout{
//     const char* name = "Erasmas"; //name cannot be modified
//     ClockOfTheLongNow apert;    //can be modified
// };

    //Member intializer Lists
//sometimes we want to intialize a member with arguments passed into a constructor. for this we use member initializer lists.
//allow you to set the value of const fields at runtime
//executes before the constructor body
struct Avout{
    Avout(const char* name, long int year_of_apert)
    : name { name }, apert { year_of_apert } { //member initializer list
    }
    void announce() const {
        printf("My Name is %s and my next apert is %d\n",name, apert.get_year());
        }
    const char* name; 
    ClockOfTheLongNow apert;
    //should order memebr init list same as in hte class definition because their constructors will be called in this order
};


int main(){
    Avout raz{ "Erasmas",3010};
    Avout jad{ "Jad",4000};
    raz.announce();
    jad.announce();
    return 0;
}