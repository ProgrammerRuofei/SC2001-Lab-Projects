#pragma once
#include "scaffold.hpp"
#include <exception>
#include <iostream>
#include <stdexcept>

inline void require(bool condition, const char* message) {
    if (!condition) throw std::runtime_error(message);
}
template<class Function>
int run_test(const char* name, Function body) {
    try {
        body();
        std::cout << "PASS: " << name << '\n';
        return 0;
    } catch (const project2::NotImplemented& e) {
        std::cerr << "PENDING: " << name << ": " << e.what() << '\n';
        return 2;
    } catch (const std::exception& e) {
        std::cerr << "FAIL: " << name << ": " << e.what() << '\n';
        return 1;
    }
}
