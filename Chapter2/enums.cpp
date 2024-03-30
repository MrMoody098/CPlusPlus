#include <cstdio>

enum class VehicleType {
    Car,
    Truck,
    Van,
    Motorcycle
};

int main(){
    VehicleType Car = VehicleType::Car;

    switch(Car){
        case VehicleType::Car:
            printf("Car\n");
            break;
        case VehicleType::Truck:
            printf("Truck\n");
            break;
        case VehicleType::Van:
            printf("Van\n");
            break;
        case VehicleType::Motorcycle:
            printf("Motorcycle\n");
            break;
    }
}