#include <cstdio>
#include <iostream> // Include the necessary header file for cout and endl


//returns absolute value
int absolute_value(int x){
    if(x>=0) return x;
    else return -x;
}

int sum(int x,int y){
    return x+y;
}

int main(){
    int num = -10;
    printf("Absolute value of %d is %d\n",num,absolute_value(num));
    int num2 = 2;
    std::cout << "Sum of " << num << " and " << num2 << " is " << sum(num,num2) << std::endl; // Use std::cout and std::endl
    return 0;
}

