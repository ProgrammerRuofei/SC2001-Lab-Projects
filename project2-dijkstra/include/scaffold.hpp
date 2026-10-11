#pragma once
#include <stdexcept>
#include <string>

namespace project2 {
// Explicit pending state; never return fabricated distances or timings.
class NotImplemented : public std::logic_error {
public:
    explicit NotImplemented(const std::string& task)
        : std::logic_error("Not implemented: " + task) {}
};
}  // namespace project2
