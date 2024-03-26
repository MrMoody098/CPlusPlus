#include <iostream>
using namespace std;



int step_function(int x){
    int result = 0;
    if(x<0){
        result = -1;
    }
    else if (x>0){
        result = 1;
    }
    return result;
}


int main() {
    int value1 = step_function(10);
    int value2 = step_function(0);
    int value3 = step_function(-10);
    cout << "Value1: " << value1 << endl;
    cout << "Value2: " << value2 << endl;
    cout << "Value3: " << value3 << endl;
    return 0;
}
