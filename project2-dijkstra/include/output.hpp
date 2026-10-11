#pragma once
#include "dijkstra.hpp"
#include <iosfwd>

namespace project2 {
// Available infrastructure. Member C owns extensions and benchmark CSV schemas.
// Does not compute results; only formats the result supplied by an algorithm.
void write_result_csv(std::ostream& output, const DijkstraResult& result);
}  // namespace project2
