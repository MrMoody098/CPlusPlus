#include <cstdio>
#include <stdexcept>
//2-1 create an enum class Operation that has values Add,Subtract,Multiply and Divide

enum class Operation{
    Add,
    Subtract,
    Multiply,
    Divide
};

// Function to convert Operation to string
const char* operationToString(Operation op) {
    switch(op) {
        case Operation::Add: return "Add";
        case Operation::Subtract: return "Subtract";
        case Operation::Multiply: return "Multiply";
        case Operation::Divide: return "Divide";
    }
    return nullptr;
}
//2-2 Create a struct calculator. it should have a single constructer that takes an Operatioin

struct Calculator{
    Operation op;

    Calculator(Operation op) : op(op) {
        printf("%s Calculator is ready to use\n", operationToString(op));
    }
    //create a caluclate function
    int calculate(int a, int b){
        switch(op){
            case Operation::Add: {
                return a+b;
            }
            case Operation::Subtract:{
                return a-b;
            }
            case Operation::Multiply:{
                return a*b;
            }
            case Operation::Divide:{
                if(b != 0) {// Check if b is not zero to avoid division by zero
                    return a/b;
                } else {
                    printf("Error: Division by zero\n");
                    return 0;
                }
            }
        }
        return 0;
    }
};

int main(){
    Calculator adder = Calculator(Operation::Add);
    printf("%d\n", adder.calculate(1,2));
    Calculator subtractor = Calculator(Operation::Subtract);
    printf("%d\n", subtractor.calculate(1,2));
    Calculator multiplier = Calculator(Operation::Multiply);
    printf("%d\n", multiplier.calculate(1,2));
    Calculator divider = Calculator(Operation::Divide);
    printf("%d\n", divider.calculate(1,0));
}