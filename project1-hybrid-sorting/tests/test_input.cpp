#include "input.hpp"

#include <algorithm>
#include <iostream>
#include <stdexcept>

int main() {
    bool passed = true;
    const auto check = [&passed](bool condition, const char* name) {
        if (!condition) {
            std::cerr << "FAIL: " << name << '\n';
            passed = false;
        }
    };

    const auto values = sc2001::generateRandomInput(1000, 100, 2001);
    check(values.size() == 1000, "requested size");
    check(std::all_of(values.begin(), values.end(), [](int value) {
        return value >= 1 && value <= 100;
    }), "values within inclusive bounds");
    check(values == sc2001::generateRandomInput(1000, 100, 2001),
          "same seed reproduces input");
    check(sc2001::generateRandomInput(0, 100, 2001).empty(), "empty input");
    check(sc2001::generateRandomInput(5, 1, 2001) == std::vector<int>(5, 1),
          "maximum value of one");
    check(sc2001::generateRandomInput(1, 1, 2001) == std::vector<int>{1},
          "single element");

    for (int invalidMaximum : {0, -1}) {
        bool rejected = false;
        try {
            sc2001::generateRandomInput(5, invalidMaximum, 2001);
        } catch (const std::invalid_argument&) {
            rejected = true;
        }
        check(rejected, "reject nonpositive maximum");
    }

    if (!passed) {
        return 1;
    }
    std::cout << "All input-generation tests passed.\n";
    return 0;
}
