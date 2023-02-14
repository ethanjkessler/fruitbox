#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <set>

#define WIDTH 17
#define HEIGHT 10

#define MAX_EVALS 1000000

struct Point {
    int x;
    int y;
};
typedef struct Point Point;

struct Match {
    Point start;
    Point end;
};
typedef struct Match Match;

Match solution[100];
int solution_count;
int solution_score;
int evaluations;

std::set<long>seen_set;

int** allocateGrid() {
    int** grid = (int**) malloc(sizeof(int*) * HEIGHT);
    for (int i = 0; i < HEIGHT; i++) {
        grid[i] = (int*) malloc(sizeof(int) * WIDTH);
    }
    return grid;
}

int** copyGrid(int** grid) {
    int** copy = allocateGrid();
    for (int i = 0; i < HEIGHT; i++) {
        memcpy(copy[i], grid[i], sizeof(int) * WIDTH);
    }
    return copy;
}

int** readGrid() {
    int** grid = allocateGrid();
    FILE* fp = fopen("gameboard.txt", "r");
    if (fp == NULL) {
        printf("Grid file not found\n");
        exit(1);
    }
    for (int i = 0; i < HEIGHT; i++) {
        for (int j = 0; j < WIDTH; j++) {
            int value = fscanf(fp, "%d", &grid[i][j]);
        }
    }
    fclose(fp);
    return grid;
}

void freeGrid(int** grid) {
    for (int i = 0; i < HEIGHT; i++) {
        free(grid[i]);
    }
    free(grid);
}

int sumRect(int** grid, Point start, Point end) {
    int sum = 0;
    for (int i = start.x; i <= end.x; i++) {
        for (int j = start.y; j <= end.y; j++) {
            sum = sum + grid[j][i];
        }
    }
    return sum;
}

int countNonZero(int** grid, Point start, Point end) {
    int count = 0;
    for (int i = start.x; i <= end.x; i++) {
        for (int j = start.y; j <= end.y; j++) {
            if (grid[j][i] != 0) {
                count++;
            }
        }
    }
    return count;
}

void zeroRect(int** grid, Point start, Point end) {
    for (int i = start.x; i <= end.x; i++) {
        for (int j = start.y; j <= end.y; j++) {
            grid[j][i] = 0;
        }
    }
}

void solveDiagonal(int** grid, Match** matches, int* count, int* score, int destructive) {
    for (int j = 0; j < WIDTH; j++) {
        for (int i = 0; i < HEIGHT; i++) {
            for (int x = j; x < WIDTH; x++) {
                for (int y = i; y < HEIGHT; y++) {
                    Point start = {j, i};
                    Point end = {x, y};
                    if (sumRect(grid, start, end) == 10) {
                        *score = (*score) + countNonZero(grid, start, end);
                        if (destructive) {
                            zeroRect(grid, start, end);
                        }
                        (*matches)[(*count)] = (Match){start, end};
                        (*count)++;
                    }
                }
            }
        }
    }
}

void generateDiagonals(int** grid, Match** matches, int* count, int* score) {
    while (1) {
        int prev_score = *score;
        solveDiagonal(grid, matches, count, score, 1);
        if (prev_score == *score) {
            break;
        }
    }
}

long computeGridHash(int** grid) {
    long hash = 0;
    for (int j = 0; j < WIDTH; j++) {
        for (int i = 0; i < HEIGHT; i++) {
            hash = 11 * hash + grid[i][j];
        }
    }
    return hash;
}

void solveDiagonalRecursive(int** grid, Match** matches, int count, int score) {
    long gridHash = computeGridHash(grid);
    if (seen_set.find(gridHash) != seen_set.end()) {
        return;
    }
    seen_set.insert(gridHash);
    for (int j = 0; j < WIDTH; j++) {
        for (int i = 0; i < HEIGHT; i++) {
            if (grid[i][j] == 0) {
                continue;
            }
            for (int x = j; x < WIDTH; x++) {
                for (int y = i; y < HEIGHT; y++) {
                    Point start = {j, i};
                    Point end = {x, y};
                    if (sumRect(grid, start, end) == 10) {
                        if (evaluations > MAX_EVALS) {
                           break;
                        }
                        evaluations++;
                        // choose
                        int** copy = copyGrid(grid);
                        zeroRect(copy, start, end);
                        (*matches)[count] = (Match){start, end};

                        // explore
                        solveDiagonalRecursive(copy, matches, count + 1, score + countNonZero(grid, start, end));

                        // unchoose
                        freeGrid(copy);
                    }
                }
            }
            // base case
            // update best if better
            if (score > solution_score) {
                solution_score = score;
                solution_count = count;
                memcpy(solution, *matches, sizeof(Match) * 100);
            }
        }
    }
}

void writeSolution(Match* matches, int count, int score, int evaluations) {
    FILE* fp = fopen("solution.txt", "w");
    char header[100];
    sprintf(header, "%d,%d,%d\n", count, score, evaluations);
    fwrite(&header, sizeof(char), strlen(header), fp);
    for (int i = 0; i < count; i++) {
        char line[25];
        Match match = matches[i];
        sprintf(line, "%d,%d->%d,%d\n", match.start.x, match.start.y,
                                            match.end.x, match.end.y);
        fwrite(&line, sizeof(char), strlen(line), fp);
    }
    fclose(fp);
}

int main() {
    int** grid = readGrid();
    Match* matches = (Match*) malloc(sizeof(Match) * 100);
    //generateDiagonals(grid, &matches, &count, &score);
    solveDiagonalRecursive(grid, &matches, 0, 0);
    printf("Score: %d\n", solution_score);
    printf("Count: %d\n", solution_count);
    writeSolution(solution, solution_count, solution_score, evaluations);
    freeGrid(grid);
}
