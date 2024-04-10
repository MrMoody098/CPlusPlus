#include <cstdio>

void printArray(int arr[], int size){
    for(int i = 0; i < size; i++){
        printf("%d\n",arr[i]);
    }
    printf("\n");


void sortInsert(int arr[], int size){
    printArray(arr, size);
    
    for(int i = 1; i < size; i++) {
        int key = arr[i];
        int j = i - 1;

        while(j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = key;
    }

    printArray(arr, size);
    }

int main() {
    int arr[] = {'a', 'b', 'c'}; int size = sizeof(arr)/sizeof(arr[0]);
    // int arr[] = {1, 3, 2, 4, 5};
    // int size = sizeof(arr)/sizeof(arr[0]);
    sortInsert(arr, size);

    return 0;
}