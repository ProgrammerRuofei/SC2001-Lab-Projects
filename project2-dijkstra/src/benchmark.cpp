#include "benchmark.hpp"
#include "dijkstra.hpp"
#include "output.hpp"

#include <chrono>
#include <iomanip>
#include <locale>
#include <random>
#include <sstream>
#include <stdexcept>
#include <utility>
#include <vector>

namespace project2 {
namespace {
std::string number(double value) {
    std::ostringstream text;
    text.imbue(std::locale::classic());
    text << std::setprecision(17) << value;
    return text.str();
}
void verify(const DijkstraResult& actual, const DijkstraResult& expected) {
    if (actual.distances != expected.distances || actual.parents != expected.parents)
        throw std::runtime_error("Algorithm result changed between calls");
}
}  // namespace

void run_benchmark(const BenchmarkConfig& config, std::ostream& output) {
    if (config.source >= config.graph.vertex_count)
        throw std::invalid_argument("Invalid source");
    if (config.mode != RunMode::Check && config.mode != RunMode::Timing &&
        config.mode != RunMode::Count) throw std::invalid_argument("Invalid mode");
    if (config.mode == RunMode::Timing && config.timing_repeats == 0)
        throw std::invalid_argument("Timing repeats must be positive");
    if (config.run_id.empty() || config.suite.empty())
        throw std::invalid_argument("Run ID and suite must be nonempty");

    // These steps are outside every timed interval.
    const auto edges = generate_connected_graph(config.graph);
    const auto matrix = make_matrix(edges);
    const auto list = make_list(edges);
    const auto matrix_answer = dijkstra_matrix(matrix, config.source);
    const auto heap_answer = dijkstra_heap(list, config.source);
    if (matrix_answer.distances != heap_answer.distances)
        throw std::runtime_error("Matrix/heap distance mismatch; measurement stopped");
    if (config.mode == RunMode::Check) {
        write_comparison_csv(output, matrix_answer, heap_answer);
        return;
    }

    const auto& spec = config.graph;
    const std::string graph_id = config.suite + ":" + kGraphGeneratorVersion +
        ":n" + std::to_string(spec.vertex_count) + ":m" + std::to_string(spec.edge_count) +
        ":seed" + std::to_string(spec.graph_seed) + ":weights" +
        std::to_string(spec.weight_min) + "-" + std::to_string(spec.weight_max) +
        ":source" + std::to_string(config.source);
    const auto n = static_cast<long double>(spec.vertex_count);
    const double density = n > 1 ? static_cast<double>(spec.edge_count / (n * (n - 1) / 2)) : 0;
    if (config.mode == RunMode::Count) {
        OperationStats a{}, b{};
        verify(dijkstra_matrix(matrix, config.source, &a), matrix_answer);
        verify(dijkstra_heap(list, config.source, &b), heap_answer);
        write_csv_row(output, {"run_id","suite","graph_id","n","m","graph_seed","algorithm",
            "min_scan_slots","matrix_scan_slots","adjacency_entries_scanned","relax_attempts",
            "relax_successes","heap_inserts","heap_extracts","heap_decreases"});
        for (const auto& entry : {std::make_pair("matrix_array", &a),
                                  std::make_pair("list_indexed_heap", &b)}) {
            const auto& s = *entry.second;
            write_csv_row(output, {config.run_id, config.suite, graph_id,
                std::to_string(spec.vertex_count),std::to_string(spec.edge_count),
                std::to_string(spec.graph_seed),entry.first,std::to_string(s.min_scan_slots),
                std::to_string(s.matrix_scan_slots),std::to_string(s.adjacency_entries_scanned),
                std::to_string(s.relax_attempts),std::to_string(s.relax_successes),
                std::to_string(s.heap_inserts),std::to_string(s.heap_extracts),
                std::to_string(s.heap_decreases)});
        }
        return;
    }

    for (std::size_t i = 0; i < config.warmup_repeats; ++i) {
        verify(dijkstra_matrix(matrix, config.source), matrix_answer);
        verify(dijkstra_heap(list, config.source), heap_answer);
    }
    write_csv_row(output, {"run_id","suite","graph_id","n","m","actual_density","graph_seed",
        "source","weight_min","weight_max","algorithm","sample_index","order_seed",
        "order_in_pair","elapsed_ms","distances_match","status"});
    std::mt19937_64 order(config.order_seed);
    auto measure = [&](bool use_matrix, std::size_t sample, unsigned position) {
        const auto start = std::chrono::steady_clock::now();
        const auto result = use_matrix ? dijkstra_matrix(matrix, config.source) :
                                         dijkstra_heap(list, config.source);
        const auto stop = std::chrono::steady_clock::now();
        const auto elapsed = std::chrono::duration<double, std::milli>(stop - start).count();
        // Result checking, serialization and destruction are outside timing.
        verify(result, use_matrix ? matrix_answer : heap_answer);
        write_csv_row(output, {config.run_id,config.suite,graph_id,std::to_string(spec.vertex_count),
            std::to_string(spec.edge_count),number(density),std::to_string(spec.graph_seed),
            std::to_string(config.source),std::to_string(spec.weight_min),std::to_string(spec.weight_max),
            use_matrix ? "matrix_array" : "list_indexed_heap",std::to_string(sample),
            std::to_string(config.order_seed),std::to_string(position),number(elapsed),"true","ok"});
    };
    for (std::size_t sample = 0; sample < config.timing_repeats; ++sample) {
        const bool matrix_first = (order() & 1) == 0;
        measure(matrix_first, sample, 0);
        measure(!matrix_first, sample, 1);
    }
}
}  // namespace project2
