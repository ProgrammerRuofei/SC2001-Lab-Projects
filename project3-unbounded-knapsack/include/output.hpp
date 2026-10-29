#pragma once

#include "types.hpp"

#include <iosfwd>

namespace project3 {
void write_problem(std::ostream& out, const Problem& problem);
void write_solution(std::ostream& out, const Problem& problem,
                    const Solution& solution, bool show_table);
}  // namespace project3
