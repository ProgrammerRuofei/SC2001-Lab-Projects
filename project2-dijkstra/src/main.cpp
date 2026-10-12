#include "benchmark.hpp"
#include "dijkstra.hpp"
#include "examples.hpp"
#include "output.hpp"

#include <charconv>
#include <exception>
#include <fstream>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>

namespace {
template<class Integer>
Integer parse_number(const std::string& text) {
    Integer value{};
    const auto parsed = std::from_chars(text.data(), text.data() + text.size(), value);
    if (parsed.ec != std::errc{} || parsed.ptr != text.data() + text.size())
        throw std::invalid_argument("Invalid integer: " + text);
    return value;
}
void help() {
    std::cout << "Project 2 Dijkstra benchmark\n"
      << "Fixed input: --demo matrix|heap\n"
      << "Random input: --n N --m M [options]\n"
      << "  --mode check|timing|count   default check\n"
      << "  --seed S --source V        defaults 2001, 0\n"
      << "  --weight-min W --weight-max W   defaults 1, 1000\n"
      << "  --warmup R --repeats R     defaults 2, 7 (timing only)\n"
      << "  --order-seed S             default 42\n"
      << "  --run-id ID --suite NAME   defaults single, manual\n"
      << "  --output FILE             default stdout; parent directory must exist\n"
      << "Timing excludes input generation, conversion, checking and CSV output.\n";
}
}  // namespace

int main(int argc, char** argv) {
    try {
        if (argc == 1 || (argc == 2 && std::string(argv[1]) == "--help")) {
            help(); return 0;
        }
        if (argc == 3 && std::string(argv[1]) == "--demo") {
            const auto graph = project2::teaching_graph();
            const std::string algorithm = argv[2];
            project2::DijkstraResult result;
            if (algorithm == "matrix") result = project2::dijkstra_matrix(project2::make_matrix(graph), 0);
            else if (algorithm == "heap") result = project2::dijkstra_heap(project2::make_list(graph), 0);
            else throw std::invalid_argument("Demo algorithm must be matrix or heap");
            project2::write_result_csv(std::cout, result);
            return 0;
        }
        project2::BenchmarkConfig config;
        std::set<std::string> seen;
        std::string output_path;
        for (int i = 1; i < argc; i += 2) {
            const std::string option = argv[i];
            if (i + 1 >= argc) throw std::invalid_argument("Missing value for " + option);
            if (!seen.insert(option).second) throw std::invalid_argument("Duplicate option: " + option);
            const std::string value = argv[i + 1];
            if (option == "--n") config.graph.vertex_count = parse_number<project2::Vertex>(value);
            else if (option == "--m") config.graph.edge_count = parse_number<std::size_t>(value);
            else if (option == "--seed") config.graph.graph_seed = parse_number<std::uint64_t>(value);
            else if (option == "--source") config.source = parse_number<project2::Vertex>(value);
            else if (option == "--weight-min") config.graph.weight_min = parse_number<project2::Weight>(value);
            else if (option == "--weight-max") config.graph.weight_max = parse_number<project2::Weight>(value);
            else if (option == "--warmup") config.warmup_repeats = parse_number<std::size_t>(value);
            else if (option == "--repeats") config.timing_repeats = parse_number<std::size_t>(value);
            else if (option == "--order-seed") config.order_seed = parse_number<std::uint64_t>(value);
            else if (option == "--run-id") config.run_id = value;
            else if (option == "--suite") config.suite = value;
            else if (option == "--output") {
                if (value.empty()) throw std::invalid_argument("Empty output path");
                output_path = value;
            } else if (option == "--mode") {
                if (value == "check") config.mode = project2::RunMode::Check;
                else if (value == "timing") config.mode = project2::RunMode::Timing;
                else if (value == "count") config.mode = project2::RunMode::Count;
                else throw std::invalid_argument("Mode must be check, timing or count");
            } else throw std::invalid_argument("Unknown option: " + option);
        }
        if (!seen.count("--n") || !seen.count("--m"))
            throw std::invalid_argument("Random input requires both --n and --m");
        if (output_path.empty()) {
            project2::run_benchmark(config, std::cout);
            if (!std::cout) throw std::runtime_error("Failed to write stdout");
        } else {
            std::ofstream output(output_path);
            if (!output) throw std::runtime_error("Cannot open output file: " + output_path);
            project2::run_benchmark(config, output);
            output.flush();
            if (!output) throw std::runtime_error("Failed to write output file");
        }
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "ERROR: " << e.what() << '\n';
        return 1;
    }
}
