#include <cstdio>

//a simple data structure made up of a series of elements or nodes
//each element contains a pointer to the next element in the linkedlist 
//the last element points to nullptr

struct Element{
    Element* next{};
    void insert_after(Element* new_element){
        new_element->next = next; // so we use the -> operator to derefrence and access our pointer and
                                  //sets the next member of new_element to the next of this
        
        next = new_element;// and then sets next of this to new_element
    }
    char prefix[2];
    short operating_number;
};

//In the next example were going to traverse a linked list of stromtroopers of type Element,printing there oprerting numbers 

int main(){
    Element trooper1,trooper2,trooper3; //initialise three stormtroopers
    trooper1.prefix[0] = 'T';
    trooper1.prefix[1] = 'K';
    trooper1.operating_number = 421;
    trooper1.insert_after(&trooper2);//insert trooper2 as next element in list after trooper2
    trooper2.prefix[0] = 'F';
    trooper2.prefix[1] = 'N';
    trooper2.operating_number = 2187;
    trooper2.insert_after(&trooper3);//insert trooper3 as next element in list after trooper2
    trooper3.prefix[0] = 'L';
    trooper3.prefix[1] = 'S';
    trooper3.operating_number = 005;
    

    //itterates through linked list
    for(Element *cursor = &trooper1;  //first your assign the cursor to the pointer to the address of trooper1
    cursor;         //the condition here checks if the cursor is nullptr as pointers will return false if they are assigned nullptr
    cursor = cursor->next) //after each itteration we set the cursor to the next element
    {
        printf("stormtrooper %c%c-%d\n",cursor->prefix[0],cursor->prefix[1],cursor->operating_number);
    }

}