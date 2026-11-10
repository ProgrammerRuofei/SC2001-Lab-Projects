#include "examples.hpp"
#include "knapsack.hpp"

#include <algorithm>
#include <iostream>
#include <limits>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {
project3::Profit enumerateItemCounts(const project3::Problem& problem,
                                     std::size_t itemIndex,
                                     int remainingCapacity) {
    if (itemIndex == problem.items.size()) return 0;

    const auto& item = problem.items[itemIndex];
    project3::Profit best = 0;
    const int maximumCount = remainingCapacity / item.weight;

    for (int count = 0; count <= maximumCount; ++count) {
        const auto currentProfit =
            static_cast<project3::Profit>(count) * item.profit;
        const auto remainingProfit = enumerateItemCounts(
            problem,
            itemIndex + 1,
            remainingCapacity - count * item.weight
        );
        best = std::max(best, currentProfit + remainingProfit);
    }

    return best;
}

project3::Profit enumerateOptimalProfit(const project3::Problem& problem) {
    project3::validate_problem(problem);
    return enumerateItemCounts(problem, 0, problem.capacity);
}

std::string describe(const project3::Problem& problem) {
    std::ostringstream out;
    out << "capacity=" << problem.capacity << ", items=";
    for (std::size_t i = 0; i < problem.items.size(); ++i) {
        if (i != 0) out << ';';
        out << '(' << problem.items[i].weight << ','
            << problem.items[i].profit << ')';
    }
    return out.str();
}

void checkEnumeratorReferenceCases() {
    const std::vector<std::pair<project3::Problem, project3::Profit>> cases{
        {project3::case_a(), 28},
        {project3::case_b(), 16},
        {project3::graph_case(), 21},
        {{0, {{4, 7}}}, 0},
        {{3, {{4, 7}, {5, 6}}}, 0},
        {{9, {{4, 7}}}, 14},
        {{10, {{6, 9}, {5, 7}}}, 14},
        {{6, {{3, 4}, {3, 5}}}, 10},
    };

    for (const auto& [problem, expected] : cases) {
        const auto actual = enumerateOptimalProfit(problem);
        if (actual != expected) {
            throw std::runtime_error(
                "Enumeration oracle failed for " + describe(problem)
            );
        }
    }
    std::cout << "PASS: independent enumeration reference cases\n";
}

void compareSolverWithEnumerator() {
    const std::vector<std::vector<project3::Item>> itemSets{
        {{1, 2}},
        {{4, 7}},
        {{2, 3}, {3, 4}},
        {{3, 4}, {3, 5}},
        {{2, 5}, {5, 12}, {7, 16}},
        {{2, 3}, {4, 7}, {5, 8}, {9, 15}},
    };

    for (const auto& items : itemSets) {
        for (int capacity = 0; capacity <= 20; ++capacity) {
            const project3::Problem problem{capacity, items};
            const auto expected = enumerateOptimalProfit(problem);
            const auto solution = project3::solve_bottom_up(problem);
            const auto actual = solution.dp.back();
            if (actual != expected) {
                throw std::runtime_error(
                    "DP/enumerator mismatch for " + describe(problem) +
                    ": expected " + std::to_string(expected) +
                    ", actual " + std::to_string(actual)
                );
            }
        }
    }
    std::cout << "PASS: DP matches independent enumeration for 126 small cases\n";
}

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
        checkEnumeratorReferenceCases();
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
        compareSolverWithEnumerator();
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
