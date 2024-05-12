#include <iostream>

// Template class declaration
template<typename T>
class Pair {
private:
    T first;
    T second;

public:
    // Constructor
    Pair(T f, T s) : first(f), second(s) {}

    // Getter methods
    T getFirst() const {
        return first;
    }

    T getSecond() const {
        return second;
    }
};

int main() {
    // Creating objects of Pair for different types
    Pair<int> intPair(10, 20);
    Pair<double> doublePair(3.14, 6.28);
    Pair<std::string> stringPair("Hello", "World");

    // Displaying values
    std::cout << "Integer pair: " << intPair.getFirst() << ", " << intPair.getSecond() << std::endl;
    std::cout << "Double pair: " << doublePair.getFirst() << ", " << doublePair.getSecond() << std::endl;
    std::cout << "String pair: " << stringPair.getFirst() << ", " << stringPair.getSecond() << std::endl;

    return 0;
}

