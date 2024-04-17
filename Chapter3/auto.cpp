#include <cstdio>

//auto type deduction
//auto is a keyword that tells the compiler to infer the type of a variable from its initializer
//this can be useful when the type is long or complex
//auto is not a type itself but a placeholder for a type

// the ompiler can determine the correct type using the intialization value

int main(){
    auto the_answer {42}; // the compiler will infer that the_answer is an int 
    auto foot {12L};
    auto rootbeer {5.0f};
    auto cheeseburger = 10.0;
    auto claim {true};
    auto car(10.4);
    return 0;
} 