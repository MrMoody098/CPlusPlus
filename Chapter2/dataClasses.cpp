#include <cstdio>

struct Book 
    {
        char name[256];
        int year;
        int pages;
        bool hardcover;
    };

struct ClockOfTHeLongNow
    {
        void add_year()
        {
            year++;
        }
        int year;
    };

int main(){
    Book my_book;
    my_book.year = 2019;
    my_book.pages = 200;
    my_book.hardcover = false;
    printf("Book year: %d\n",my_book.year);

    ClockOfTHeLongNow clock;
    clock.year = 2020;
    printf("Year: %d\n",clock.year);
    clock.add_year();
    printf("Year: %d\n",clock.year);
}

void dataTypes(){
    
}