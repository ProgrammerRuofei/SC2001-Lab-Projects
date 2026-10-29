#include "examples.hpp"
#include "output.hpp"

#include <iostream>
#include <sstream>
#include <stdexcept>

namespace {
void require(bool condition, const char* message) {
    if (!condition) throw std::runtime_error(message);
}
void rejects(const project3::Problem& problem) {
    try { project3::validate_problem(problem); }
    catch (const std::invalid_argument&) { return; }
    throw std::runtime_error("Invalid problem was accepted");
}
}  // namespace

int main() {
    try {
        project3::validate_problem(project3::case_a());
        project3::validate_problem(project3::case_b());
        project3::validate_problem({0, {{1, 1}}});
        rejects({-1, {{1, 1}}});
        rejects({4, {}});
        rejects({4, {{0, 1}}});
        rejects({4, {{-1, 1}}});
        rejects({4, {{1, 0}}});
        rejects({4, {{1, -1}}});
        std::ostringstream out;
        project3::write_solution(out, {1, {{2, 3}}}, {{0, 0}}, true);
        require(out.str() == "maximum_profit=0\ncapacity,maximum_profit\n0,0\n1,0\n",
                "Unexpected table format");
        bool rejected = false;
        try { project3::write_solution(out, {1, {{2, 3}}}, {{}}, false); }
        catch (const std::invalid_argument&) { rejected = true; }
        require(rejected, "Incomplete solution table was accepted");
        std::cout << "PASS: framework validation and output; solver not assessed here\n";
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "FAIL: " << e.what() << '\n';
        return 1;
    }
}
