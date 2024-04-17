#include <cstdio>
// add a read_from and write to function
void BufferOverflows(){
    //const methods are read only and adds an extra sense of security

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

struct BuffMan(){
     //for arrays and pointers,you can access arbitaty array elements with the bracket opetator ([]) or with pointer arithmetic.
    char lower[] = "abc?e";
    char upper[] = "ABC?e";
    char* upper_ptr = upper; //equivelent to &upper[0]

    
     const auto read(auto target[]){
        switch {
            case:lower,
            printf("%c",lower[]);
            return lower
        }
    }


};

int main(){
    BuffMan bm = BuffMan();
    bm.read("abc?e");
    return 0;
}