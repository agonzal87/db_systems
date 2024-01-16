/* Alexis Gonzalez
 * CSCI 211 - OOP in C++
 * Assignment 6 - 8 Queens in 1D
 * */

#include <iostream>
using namespace std;

// Function to check if placing a queen in column c is safe
bool ok(int q[], int c) {
    for (int i = 0; i < c; i++) {
        // Check if the queen in the current column conflicts with any previous queens
        if (q[i] == q[c] || (c - i) == abs(q[c] - q[i])) {
            return false;
        }
    }
    return true; // No conflicts, it's safe to place a queen
}

// Function to print the chessboard with queens placed
void print(int q[]) {
    static int count = 0;
    cout << "Solution #" << ++count << endl;
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
            // Print '1' where queens are placed, '0' otherwise
            if (q[j] == i) {
                cout << "1 ";
            }
            else {
                cout << "0 ";
            }
        }
        cout << endl;
    }
}

int main() {
    // Create the array to represent the chessboard
    int q[8] = {0}, c = 0;
    q[0] = 0; // Place the first queen in the first column (0-indexed)

    while (c >= 0) {
        // If queens have been placed in all columns, print the solution
        if (c > 7) {
            print(q);
            c--;
            q[c]++;
        }
        // If the current row in the current column exceeds the board size, backtrack
        else if (q[c] > 7) {
            q[c] = 0;
            c--;
            if (c == -1) return 0; // If backtracked beyond the first column, exit
            q[c]++;
        }
        // If placing a queen in the current column is safe, move to the next column
        else if (ok(q, c)) {
            c++;
        }
        // If there's a conflict, move to the next row in the current column
        else {
            q[c]++;
        }
    }
    return 0;
}
