#include <iostream>
#include <vector>
#include <string>
#include <sys/stat.h>
#include <bits/stdc++.h>
#include <chrono>
#include <cmath>

using namespace std;
using namespace std::chrono;

long long steps = 0;

struct Point {
    int row, col;
};

// Fungsi Helper 
void printBoard(Point* positionQueen, int currentN, int totalN) {
    cout << "START_BOARD" << endl;
    for (int i = 0; i < totalN; i++) {
        for (int j = 0; j < totalN; j++) {
            bool isQueen = false;
            // Cek apakah di (i, j) ada Queen
            for (int k = 0; k < currentN; k++) {
                if (positionQueen[k].row == i && positionQueen[k].col == j) {
                    isQueen = true;
                    break;
                }
            }
            cout << (isQueen ? "1" : "0") << (j == totalN - 1 ? "" : ",");
        }
        cout << endl;
    }
    cout << "END_BOARD" << endl;
}

bool checkDiagonal(int rowA, int colA, int rowB, int colB) {
    return (abs(colA - colB) == 1 && abs(rowA - rowB) == 1);
}

bool isValid(Point* positionQueen, char* color, int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = i + 1; j < n; j++) {
            if (positionQueen[i].row == positionQueen[j].row || 
                positionQueen[i].col == positionQueen[j].col || 
                color[i] == color[j] || 
                checkDiagonal(positionQueen[i].row, positionQueen[i].col, positionQueen[j].row, positionQueen[j].col)) {
                return false;
            }
        }
    }
    return true;
}

void optimized(Point* coordinate, char* color, int n, char** map, bool* valid){
    // Optimized: search by row O(n^n)
    int rowNow = 0, colNow = 0;
    
    for(int i = 0; i < n; i++){
        coordinate[i] = {i, 0};
        color[i] = map[i][0];
    }
    int shifted = n-1;

    if(isValid(coordinate, color, n)){
        *valid = true;
        steps++;
        return;
    }else{
        bool found = false;

        while(!found){
            shifted = n - 1;
            while(shifted >= 0 && coordinate[shifted].col == n-1) shifted--;
            //kalau indeks udh mentok, mundurin row yg digeser
            if(shifted < 0) found = true; // sudah mentok, tidak ada hasil
            else{
                coordinate[shifted].col++;
                color[shifted] = map[shifted][coordinate[shifted].col];
                
                if(isValid(coordinate, color, n)){
                    *valid = true;
                    found = true;
                }

                int temp = shifted + 1;
                while(temp < n){
                    coordinate[temp].col = 0; // mulai dari queen [shifted-1], mulai dari col = 0 semua.
                    color[temp] = map[temp][coordinate[temp].col];
                    temp++;
                }
                steps++;
            }
            if (steps % (5*n*n+1) == 0) printBoard(coordinate, n, n);
        }
    }
}

void algoritmaBF(Point* coordinate, char* color, int n, char** map, bool* valid) {
    // Pure brute force, kompleksitas O(C(n*n, n))
    int d1[n];
    for(int i = 0; i < n; i++){
        coordinate[i] = {0, i};
        color[i] = map[0][i];
        d1[i] = i;
    }

    int shifted = n-1;
    
    if(isValid(coordinate, color, n)){
        *valid = true;
        steps++;
        return;
    }else{
        bool found = false;

        while(!found){
            shifted = n - 1;
            while(shifted >= 0 && d1[shifted] >= (n*n - n + shifted)) shifted--;
            //kalau indeks udh mentok, mundurin
            if(shifted < 0) found = true; // sudah mentok, tidak ada hasil
            else{
                d1[shifted]++;
                coordinate[shifted] = {d1[shifted] / n, d1[shifted] % n};
                color[shifted] = map[coordinate[shifted].row][coordinate[shifted].col];
                
                if(isValid(coordinate, color, n)){
                    *valid = true;
                    found = true;
                }

                int temp = shifted + 1;
                while(temp < n){
                    d1[temp] = d1[temp-1] + 1; // mulai dari queen [shifted-1], buat sebelahan semua sampai queen[n]
                    coordinate[temp] = {d1[temp]/n, d1[temp]%n};
                    color[temp] = map[coordinate[temp].row][coordinate[temp].col];
                    temp++;
                }
                steps++;
            }
            if (steps % (2*n*n*n) == 0) printBoard(coordinate, n, n);
        }
    }
}

int main(int argc, char* argv[]){
    if (argc < 3) return 1;
    string filename = argv[1];
    string algo = argv[2];

    ifstream f(filename);
    if (!f.is_open()) return 1;

    vector<string> lines;
    string s;
    while (getline(f, s)) if (!s.empty()) lines.push_back(s);
    f.close();

    int n = lines.size();
    char** map = new char*[n];
    for (int i = 0; i < n; i++) {
        map[i] = new char[n];
        for (int j = 0; j < n; j++) map[i][j] = lines[i][j];
    }

    Point* positionQueen = new Point[n];
    char* color = new char[n];
    bool solutionExist = false;

    auto start = high_resolution_clock::now();
    if (algo == "bruteforce") algoritmaBF(positionQueen, color, n, map, &solutionExist);
    else optimized(positionQueen, color, n, map, &solutionExist);

    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<milliseconds>(stop - start);

    string mode = "";
    if(argc == 4) mode = argv[3];

    if (solutionExist) {
        cout << "RESULT:FOUND" << endl;
        printBoard(positionQueen, n, n);

        if(mode == "save"){
            string path = "../test/";
            string solutionFile;
            int iter = 1;
            struct stat sb;

            // Cari angka yang belum dipakai
            do {
                solutionFile = path + "solution" + to_string(iter) + ".txt";
                iter++;
            } while (stat(solutionFile.c_str(), &sb) == 0); 


            ofstream NewFile(solutionFile);
            if(!NewFile){
                cerr << "Error opening the file for writing.";
            }

            for(int i = 0; i < n; i++){
                for(int j = 0; j < n; j++){
                    bool isQueen = false;
                    // Cek apakah di (i, j) ada Queen
                    for (int k = 0; k < n; k++) {
                        if (positionQueen[k].row == i && positionQueen[k].col == j) {
                            isQueen = true;
                            break;
                        }
                    }
                    NewFile << (isQueen ? '#' : map[i][j]) << (j == n - 1 ? "" : " ");
                }
                if(i < n-1) NewFile << endl;
            }

            NewFile.close();
            cout << "NAMA FILE:" << solutionFile << endl;
        }
    } else {
        cout << "RESULT:NOT_FOUND" << endl;
    }
    
    // KIRIM STATS KE PYTHON
    cout << "STEPS:" << steps << endl;
    cout << "TIME:" << duration.count() << endl;
    // Cleanup
    for (int i = 0; i < n; i++) delete[] map[i];
    delete[] map;
    delete[] positionQueen;
    delete[] color;

    return 0;
}