#include "output.hpp"
#include <ostream>
#include <stdexcept>

namespace project2 {
void write_result_csv(std::ostream& output, const DijkstraResult& result) {
    if (result.distances.size() != result.parents.size()) {
        throw std::invalid_argument("Result arrays have different lengths");
    }
    output << "vertex,distance,parent\n";
    for (Vertex v = 0; v < result.distances.size(); ++v) {
        output << v << ',';
        if (result.distances[v] == kInfinity) output << "INF";
        else output << result.distances[v];
        output << ',';
        if (result.parents[v] == kNoVertex) output << "NONE";
        else output << result.parents[v];
        output << '\n';
    }
}
}  // namespace project2
