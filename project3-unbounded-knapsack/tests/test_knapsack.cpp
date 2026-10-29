#include "examples.hpp"
#include "knapsack.hpp"

#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>

namespace {
void check(const std::string& name, const project3::Problem& problem,
           project3::Profit expected) {
    const auto solution = project3::solve_bottom_up(problem);
    if (solution.dp.size() != static_cast<std::size_t>(problem.capacity) + 1 ||
        solution.dp.front() != 0 || solution.dp.back() != expected)
        throw std::runtime_error("Wrong solution: " + name);
    for (std::size_t c = 1; c < solution.dp.size(); ++c) {
        if (solution.dp[c] < solution.dp[c - 1])
            throw std::runtime_error("Profit decreases with capacity: " + name);
    }
    std::cout << "PASS: " << name << '\n';
}
}  // namespace

int main() {
    try {
        check("Q4(a)", project3::case_a(), 28);
        check("Q4(b)", project3::case_b(), 16);
        check("Q2 capacity", project3::graph_case(), 21);
        check("zero capacity", {0, {{4, 7}}}, 0);
        check("nothing fits", {3, {{4, 7}, {5, 6}}}, 0);
        check("repeated item with unused capacity", {9, {{4, 7}}}, 14);
        check("density greedy counterexample", {10, {{6, 9}, {5, 7}}}, 14);
        check("same weight, different profit", {6, {{3, 4}, {3, 5}}}, 10);
        check("profit needs 64 bits", {2, {{1, std::numeric_limits<int>::max()}}},
              2LL * std::numeric_limits<int>::max());
        const auto b = project3::solve_bottom_up(project3::case_b());
        const std::vector<project3::Profit> expected_b{0, 0, 0, 0, 0, 7, 7, 9, 9, 9, 14, 14, 16};
        if (b.dp != expected_b) throw std::runtime_error("Wrong intermediate states for Q4(b)");
        // TODO (Member B): add an independent small-case enumeration oracle.
        // Enumerate item counts, not this same DP recurrence, then compare profits.
        std::cout << "PASS: initial solution acceptance cases\n";
        return 0;
    } catch (const project3::NotImplemented& e) {
        std::cerr << "PENDING: solution acceptance not completed: " << e.what() << '\n';
        return 2;
    } catch (const std::exception& e) {
        std::cerr << "FAIL: " << e.what() << '\n';
        return 1;
    }
}
