#pragma once
#include "dijkstra.hpp"
#include <iosfwd>
#include <string>
#include <vector>

namespace project2 {
// CSV quoting supports commas, quotes and newlines in metadata.
void write_csv_row(std::ostream& output, const std::vector<std::string>& fields);
void write_result_csv(std::ostream& output, const DijkstraResult& result);
void write_comparison_csv(std::ostream& output, const DijkstraResult& matrix,
                          const DijkstraResult& heap);
}  // namespace project2
