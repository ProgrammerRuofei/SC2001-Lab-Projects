#include "dijkstra.hpp"
#include "examples.hpp"
#include "output.hpp"
#include "scaffold.hpp"

#include <exception>
#include <iostream>
#include <string>

int main(int argc, char** argv) {
    // OWNER: Member C. Add full argument parsing for BenchmarkConfig and call
    // run_benchmark once generation and measurements are implemented.
    if (argc == 1 || (argc == 2 && std::string(argv[1]) == "--help")) {
        std::cout << "Project 2 scaffold\n"
                  << "Available: --help, --demo matrix, --demo heap\n"
                  << "Demo uses the fixed five-vertex input; pending algorithms exit 2.\n"
                  << "Random input, timing/count modes and batch CLI are pending.\n";
        return 0;
    }
    try {
        if (argc == 3 && std::string(argv[1]) == "--demo") {
            const auto graph = project2::teaching_graph();
            const std::string algorithm = argv[2];
            project2::DijkstraResult result;
            if (algorithm == "matrix") {
                result = project2::dijkstra_matrix(project2::make_matrix(graph), 0);
            } else if (algorithm == "heap") {
                result = project2::dijkstra_heap(project2::make_list(graph), 0);
            } else {
                throw std::invalid_argument("Demo algorithm must be matrix or heap");
            }
            project2::write_result_csv(std::cout, result);
            return 0;
        }
        throw std::invalid_argument("Unsupported arguments; use --help");
    } catch (const project2::NotImplemented& e) {
        std::cerr << "PENDING: " << e.what() << '\n';
        return 2;
    } catch (const std::exception& e) {
        std::cerr << "ERROR: " << e.what() << '\n';
        return 1;
    }
}
