#pragma once
#include "generation.hpp"
#include <iosfwd>

namespace project2 {
enum class RunMode { Check, Timing, Count };
struct BenchmarkConfig {
    GraphSpec graph;
    Vertex source = 0;
    std::size_t warmup_repeats = 2;
    std::size_t timing_repeats = 7;
    std::uint64_t order_seed = 42;
    RunMode mode = RunMode::Check;
};
// Member C: implement one graph, both algorithms, and output for the selected mode.
// Check mode writes distances; timing/count modes use the documented CSV schemas.
void run_benchmark(const BenchmarkConfig& config, std::ostream& output);
}  // namespace project2
