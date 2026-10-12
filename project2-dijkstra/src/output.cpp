#include "output.hpp"
#include <ostream>
#include <stdexcept>
#include <utility>

namespace project2 {
namespace {
void validate_result(const DijkstraResult& result) {
    if (result.distances.size() != result.parents.size())
        throw std::invalid_argument("Result arrays have different lengths");
}
std::vector<std::string> result_fields(const DijkstraResult& result, Vertex v) {
    return {std::to_string(v), result.distances[v] == kInfinity ? "INF" :
            std::to_string(result.distances[v]), result.parents[v] == kNoVertex ?
            "NONE" : std::to_string(result.parents[v])};
}
}  // namespace

void write_csv_row(std::ostream& output, const std::vector<std::string>& fields) {
    for (std::size_t i = 0; i < fields.size(); ++i) {
        if (i) output << ',';
        const auto& field = fields[i];
        if (field.find_first_of(",\"\r\n") == std::string::npos) output << field;
        else {
            output << '"';
            for (const char c : field) {
                if (c == '"') output << '"';
                output << c;
            }
            output << '"';
        }
    }
    output << '\n';
}
void write_result_csv(std::ostream& output, const DijkstraResult& result) {
    validate_result(result);
    write_csv_row(output, {"vertex", "distance", "parent"});
    for (Vertex v = 0; v < result.distances.size(); ++v)
        write_csv_row(output, result_fields(result, v));
}
void write_comparison_csv(std::ostream& output, const DijkstraResult& matrix,
                          const DijkstraResult& heap) {
    validate_result(matrix); validate_result(heap);
    if (matrix.distances.size() != heap.distances.size())
        throw std::invalid_argument("Comparison result sizes differ");
    write_csv_row(output, {"algorithm", "vertex", "distance", "parent"});
    for (const auto& entry : {std::make_pair("matrix_array", &matrix),
                              std::make_pair("list_indexed_heap", &heap)}) {
        for (Vertex v = 0; v < entry.second->distances.size(); ++v) {
            auto fields = result_fields(*entry.second, v);
            fields.insert(fields.begin(), entry.first);
            write_csv_row(output, fields);
        }
    }
}
}  // namespace project2
