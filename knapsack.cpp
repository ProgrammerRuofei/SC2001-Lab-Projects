// SC2001 Project 3: unbounded knapsack by dynamic programming
//
// A knapsack has capacity C. There are n types of objects; an object of type i
// has weight w[i] and profit p[i], and every type has an unlimited supply.
// P(C) = the largest total profit of objects whose total weight is at most C.
//
// Recursive definition (question 1):
//   P(c) = 0                                        if w[i] > c for every type i
//   P(c) = max { p[i] + P(c - w[i]) : w[i] <= c }   otherwise
//
// This program
//   1. solves the instances of questions (2), (4a) and (4b),
//   2. tests the DP against brute force on random instances (experiment 1),
//   3. measures running times and writes them to results/*.csv (experiments 2-4).
//
// Build and run:   g++ -std=c++17 -O2 knapsack.cpp -o knapsack
//                  ./knapsack > results/output.txt

#include <algorithm>
#include <chrono>
#include <cstdio>
#include <filesystem>
#include <random>
#include <vector>
using namespace std;


// ============================================================================
// The algorithm (question 3): bottom-up dynamic programming
// ============================================================================

// Returns the table P[0..C]: P[c] = maximum profit for capacity c.
vector<long long> knapsack(int C, const vector<int>& w,
                           const vector<int>& p) {
    int n = w.size();
    vector<long long> P(C + 1, 0);           // P[0] = 0

    for (int c = 1; c <= C; c++) {           // smaller capacities first
        long long best = 0;                  // stays 0 if no type fits into c
        for (int i = 0; i < n; i++) {        // try every type i that fits
            if (w[i] <= c) {
                best = max(best, p[i] + P[c - w[i]]);
            }
        }
        P[c] = best;
    }
    return P;
}

// Finds the objects that give the profit P[C]: count[i] = number of objects of type i.
// If P[c] == p[i] + P[c - w[i]], one object of type i belongs to a best packing
// for capacity c, so we take it and continue with capacity c - w[i].
vector<int> findPacking(int C, const vector<int>& w, const vector<int>& p,
                        const vector<long long>& P) {
    int n = w.size();
    vector<int> count(n, 0);
    int c = C;

    while (P[c] > 0) {                       // P[c] == 0: no object fits any more
        for (int i = 0; i < n; i++) {
            if (w[i] <= c && P[c] == p[i] + P[c - w[i]]) {
                count[i]++;
                c = c - w[i];
                break;
            }
        }
    }
    return count;
}


// ============================================================================
// Two slow methods, only used to test the DP and to compare running times
// ============================================================================

// The recursive definition evaluated directly, without a table. It solves the
// same subproblems again and again, so its time grows exponentially with C.
long long naiveCalls = 0;                    // number of calls (experiment 4)

long long naiveRecursion(int c, const vector<int>& w, const vector<int>& p) {
    naiveCalls++;
    int n = w.size();
    long long best = 0;
    for (int i = 0; i < n; i++) {
        if (w[i] <= c) {
            best = max(best, p[i] + naiveRecursion(c - w[i], w, p));
        }
    }
    return best;
}

// Brute force: try every number k of objects of type i, then the types after i.
// It does not use the recursive definition, so it is an independent check.
long long bruteForce(int i, int c, const vector<int>& w, const vector<int>& p) {
    int n = w.size();
    if (i == n) {
        return 0;
    }
    long long best = 0;
    for (int k = 0; k * w[i] <= c; k++) {
        best = max(best, k * p[i] + bruteForce(i + 1, c - k * w[i], w, p));
    }
    return best;
}


// ============================================================================
// Questions (2) and (4): solve one instance and print the result
// ============================================================================

void solveAndPrint(const char* title, int C, const vector<int>& w, const vector<int>& p) {
    int n = w.size();
    vector<long long> P = knapsack(C, w, p);
    vector<int> count = findPacking(C, w, p, P);

    printf("%s: capacity C = %d\n", title, C);
    printf("  type i :");
    for (int i = 0; i < n; i++) printf("%3d", i);
    printf("\n  w[i]   :");
    for (int i = 0; i < n; i++) printf("%3d", w[i]);
    printf("\n  p[i]   :");
    for (int i = 0; i < n; i++) printf("%3d", p[i]);
    printf("\n\n  c      :");
    for (int c = 0; c <= C; c++) printf("%3d", c);
    printf("\n  P(c)   :");
    for (int c = 0; c <= C; c++) printf("%3lld", P[c]);
    printf("\n\n");

    printf("  P(%d) = %lld\n", C, P[C]);
    printf("  packing:");
    int weight = 0, profit = 0;
    const char* separator = " ";
    for (int i = 0; i < n; i++) {
        if (count[i] > 0) {
            printf("%s%d x type %d", separator, count[i], i);
            separator = " + ";
            weight += count[i] * w[i];
            profit += count[i] * p[i];
        }
    }
    printf("\n  total weight %d <= %d, total profit %d\n\n", weight, C, profit);
}


// ============================================================================
// Experiment 1: correctness on random instances
// ============================================================================

mt19937 rng(2001);                           // fixed seed: the same instances on every run

int randomInt(int low, int high) {
    return uniform_int_distribution<int>(low, high)(rng);
}

void testCorrectness() {
    int tests = 10000, wrong = 0;
    for (int t = 0; t < tests; t++) {
        // A random small instance: 1-5 types, weights 1-12, profits 1-20, capacity 1-40.
        int n = randomInt(1, 5), C = randomInt(1, 40);
        vector<int> w(n), p(n);
        for (int i = 0; i < n; i++) {
            w[i] = randomInt(1, 12);
            p[i] = randomInt(1, 20);
        }

        vector<long long> P = knapsack(C, w, p);
        vector<int> count = findPacking(C, w, p, P);
        long long weight = 0, profit = 0;
        for (int i = 0; i < n; i++) {
            weight += count[i] * w[i];
            profit += count[i] * p[i];
        }

        // P(C) must equal brute force, and the packing must fit and be worth P(C).
        if (P[C] != bruteForce(0, C, w, p) || weight > C || profit != P[C]) {
            wrong++;
        }
    }
    printf("  %d random instances (n <= 5, w <= 12, p <= 20, C <= 40)\n", tests);
    printf("  P(C) equal to brute force, packing fits and is worth P(C): %d wrong\n\n", wrong);
}


// ============================================================================
// Experiments 2-4: running time
// ============================================================================

volatile long long sink;                     // results go here, so the compiler cannot skip a timed call

double millisecondsSince(chrono::steady_clock::time_point start) {
    return chrono::duration<double, milli>(chrono::steady_clock::now() - start).count();
}

// Time of knapsack(C, w, p) in milliseconds: the median of 5 runs. Each run calls it
// `repeats` times and divides by `repeats`, for inputs too fast to time with one call.
double timeDP(int C, const vector<int>& w, const vector<int>& p, int repeats) {
    vector<double> times;
    for (int run = 0; run < 5; run++) {
        auto start = chrono::steady_clock::now();
        for (int r = 0; r < repeats; r++) {
            sink = knapsack(C, w, p)[C];
        }
        times.push_back(millisecondsSince(start) / repeats);
    }
    sort(times.begin(), times.end());
    return times[2];
}

// Time of naiveRecursion(C, w, p) in milliseconds: the median of 3 runs.
double timeNaive(int C, const vector<int>& w, const vector<int>& p) {
    vector<double> times;
    for (int run = 0; run < 3; run++) {
        auto start = chrono::steady_clock::now();
        sink = naiveRecursion(C, w, p);
        times.push_back(millisecondsSince(start));
    }
    sort(times.begin(), times.end());
    return times[1];
}

// The first n elements of v.
vector<int> firstN(const vector<int>& v, int n) {
    return vector<int>(v.begin(), v.begin() + n);
}

void runTimingExperiments() {
    filesystem::create_directory("results");

    // 1000 random object types, weights and profits from 1 to 1000.
    // An experiment with n types uses the first n of them.
    vector<int> w(1000), p(1000);
    for (int i = 0; i < 1000; i++) {
        w[i] = randomInt(1, 1000);
        p[i] = randomInt(1, 1000);
    }

    // Experiment 2: time against C, with n = 100 types.
    FILE* file = fopen("results/time_vs_C.csv", "w");
    fprintf(file, "C,n,time_ms\n");
    for (int C = 100000; C <= 1000000; C += 100000) {
        fprintf(file, "%d,%d,%.3f\n", C, 100, timeDP(C, firstN(w, 100), firstN(p, 100), 1));
    }
    fclose(file);

    // Experiment 3: time against n, with C = 100,000.
    file = fopen("results/time_vs_n.csv", "w");
    fprintf(file, "C,n,time_ms\n");
    for (int n = 100; n <= 1000; n += 100) {
        fprintf(file, "%d,%d,%.3f\n", 100000, n, timeDP(100000, firstN(w, n), firstN(p, n), 1));
    }
    fclose(file);

    // Experiment 4: plain recursion against the DP, on the instance of question (2).
    vector<int> w2 = {4, 5, 8}, p2 = {7, 6, 9};
    file = fopen("results/naive_vs_dp.csv", "w");
    fprintf(file, "C,naive_calls,naive_ms,dp_ms\n");
    for (int C = 40; C <= 100; C += 5) {
        naiveCalls = 0;
        naiveRecursion(C, w2, p2);           // one run to count the calls
        long long calls = naiveCalls;
        double naiveMs = timeNaive(C, w2, p2);
        double dpMs = timeDP(C, w2, p2, 100000);
        fprintf(file, "%d,%lld,%.6f,%.6f\n", C, calls, naiveMs, dpMs);
    }
    fclose(file);
}


int main() {
    printf("=== Questions (2) and (4): instances from the project sheet ===\n\n");
    solveAndPrint("Question (2)", 15, {4, 5, 8}, {7, 6, 9});
    solveAndPrint("Question (4a)", 16, {4, 5, 8}, {7, 6, 9});
    solveAndPrint("Question (4b)", 12, {5, 6, 7}, {7, 6, 9});

    printf("=== Experiment 1: correctness ===\n");
    testCorrectness();

    printf("=== Experiments 2-4: running time ===\n");
    runTimingExperiments();
    printf("  results/time_vs_C.csv, results/time_vs_n.csv, results/naive_vs_dp.csv\n");
    return 0;
}
