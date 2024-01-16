/* Alexis Gonzalez
 * CSCI 211 - OOP in C++
 * Assignment 8 - Stable Marriage
 * */

#include <iostream>
using namespace std;

// Function to check if the current partial solution is stable
bool ok(int q[], int col)
{
    // Preference matrix for men (mp) and women (wp)
    int mp[3][3] = {{0, 2, 1}, // Man 0 likes women 0 the most but women 1 the least
                    {0, 2, 1},
                    {1, 2, 0}};

    int wp[3][3] = {{2, 1, 0}, // Women 0 likes man 2 the most but man 0 the least
                    {0, 1, 2},
                    {2, 0, 1}};

    int newMan, newWoman, currentMan, currentWoman;

    newMan = col;
    newWoman = q[col];

    // If the new woman has been used, then return false
    for (int i = 0; i < col; i++) {
        currentMan = i;
        currentWoman = q[i];
        if (newWoman == currentWoman) {
            return false;
        }
        // Check stability conditions based on preferences
        if ((mp[currentMan][newWoman] < mp[currentMan][currentWoman]) && (wp[newWoman][currentMan] < wp[newWoman][newMan])) {
            return false;
        }
        if ((mp[newMan][currentWoman] < mp[newMan][newWoman]) && (wp[currentWoman][newMan] < wp[currentWoman][currentMan])) {
            return false;
        }
    }
    return true; // The current partial solution is stable
}

// Function to print the solution
void print(int q[]) {
    static int count = 0;
    cout << "Solution #" << ++count << endl;
    cout << "Man\tWoman" << endl;
    for (int i = 0; i < 3; i++) {
        cout << i << "\t" << q[i] << endl;
    }
    cout << endl;
}

int main() {

    // Start with the first man
    int newMan = 0;
    int q[3] = {0}; // Array to store the current solution

    // If we backtrack beyond the first man, we are done
    while (newMan >= 0) {

        // If we have moved beyond the last column
        if (newMan == 3) {
            print(q); // Print the result
            newMan--; // Backtrack
            q[newMan]++;
        }
            // If we have moved beyond the last row
        else if (q[newMan] == 3) {
            q[newMan] = 0; // Reset new woman
            newMan--; // Backtrack
            if (newMan == -1) {
                return 0; // Done with all solutions
            }
            q[newMan]++;
        }
            // Check if the marriage is stable
        else if (ok(q, newMan)) {
            newMan++; // Move to the next column if ok
        }
        else {
            q[newMan]++; // Move to the new row if not ok
        }
    }
    return 0;
}
