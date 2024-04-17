#include <cstdio>
//the this pointer points to this object instance similar to java where 
//when you want to access an attribute of this instance you say this.attribute
struct Element{
    Element* next{};
    void insert_after(Element* new_element){
        new_element->next = this->next;
        this->next = new_element;
    }
    char prefix[2];
    short operating_number;
}

//sometimes we need the this pointer tot resolve ambiguity between members and arguments as demonstrated below

struct ClockOfTheLongNow{
    bool set_year(int year){ //the year argument has the same name as the year member
        if(year< 2024)return false;
        this->year = year; // you can disambiguate using the this pointer
        return true;
    }
    private:
        int year; //year member has same name as argument
}