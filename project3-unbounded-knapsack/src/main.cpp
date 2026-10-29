#include "examples.hpp"
#include "knapsack.hpp"
#include "output.hpp"

#include <charconv>
#include <iostream>
#include <set>
#include <string>
#include <vector>

namespace {
int integer(const std::string& text) {
    int value{};
    const auto parsed = std::from_chars(text.data(), text.data() + text.size(), value);
    if (parsed.ec != std::errc{} || parsed.ptr != text.data() + text.size())
        throw std::invalid_argument("Invalid integer: " + text);
    return value;
}

std::vector<int> integers(const std::string& text) {
    std::vector<int> values;
    std::size_t start = 0;
    while (true) {
        const auto end = text.find(',', start);
        values.push_back(integer(text.substr(start, end - start)));
        if (end == std::string::npos) return values;
        start = end + 1;
    }
}

void help() {
    std::cout << "Project 3: Unbounded Knapsack (C++17)\n"
              << "  --case a|b|graph [--table]\n"
              << "  --capacity C --weights W1,W2,... --profits P1,P2,... [--table]\n"
              << "a: Q4(a), C=16; b: Q4(b), C=12; graph: Q2 data, C=15\n"
              << "--table prints all DP states; graph selects data, not a drawing.\n"
              << "Exit codes: 0 success; 1 invalid input/error; 2 solver pending.\n";
}
}  // namespace

int main(int argc, char** argv) {
    try {
        if (argc == 1 || (argc == 2 && std::string(argv[1]) == "--help")) {
            help();
            return 0;
        }
        std::set<std::string> seen;
        std::string case_name;
        int capacity = 0;
        std::vector<int> weights, profits;
        bool show_table = false;
        for (int i = 1; i < argc; ++i) {
            const std::string option = argv[i];
            if (!seen.insert(option).second)
                throw std::invalid_argument("Duplicate option: " + option);
            if (option == "--table") { show_table = true; continue; }
            if (option != "--case" && option != "--capacity" &&
                option != "--weights" && option != "--profits")
                throw std::invalid_argument("Unknown option: " + option);
            if (++i >= argc) throw std::invalid_argument("Missing value for " + option);
            const std::string value = argv[i];
            if (option == "--case") case_name = value;
            else if (option == "--capacity") capacity = integer(value);
            else if (option == "--weights") weights = integers(value);
            else profits = integers(value);
        }
        project3::Problem problem;
        if (seen.count("--case")) {
            if (seen.count("--capacity") || seen.count("--weights") || seen.count("--profits"))
                throw std::invalid_argument("Use either --case or custom input");
            if (case_name == "a") problem = project3::case_a();
            else if (case_name == "b") problem = project3::case_b();
            else if (case_name == "graph") problem = project3::graph_case();
            else throw std::invalid_argument("Case must be a, b, or graph");
        } else {
            if (!seen.count("--capacity") || !seen.count("--weights") || !seen.count("--profits"))
                throw std::invalid_argument("Custom input needs capacity, weights, and profits");
            if (weights.size() != profits.size())
                throw std::invalid_argument("Weights and profits must have equal lengths");
            problem.capacity = capacity;
            for (std::size_t i = 0; i < weights.size(); ++i)
                problem.items.push_back({weights[i], profits[i]});
        }
        project3::validate_problem(problem);
        project3::write_problem(std::cout, problem);
        const auto solution = project3::solve_bottom_up(problem);
        project3::write_solution(std::cout, problem, solution, show_table);
        return 0;
    } catch (const project3::NotImplemented& e) {
        std::cerr << "PENDING: " << e.what() << '\n';
        return 2;
    } catch (const std::exception& e) {
        std::cerr << "ERROR: " << e.what() << '\n';
        return 1;
    }
}
