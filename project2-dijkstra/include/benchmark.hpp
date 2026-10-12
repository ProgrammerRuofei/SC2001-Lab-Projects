#pragma once
#include "generation.hpp"
#include <iosfwd>
#include <string>

namespace project2 {
enum class RunMode { Check, Timing, Count };
struct BenchmarkConfig {
    GraphSpec graph{0, 0, 2001};
    Vertex source = 0;
    std::size_t warmup_repeats = 2;
    std::size_t timing_repeats = 7;
    std::uint64_t order_seed = 42;
    RunMode mode = RunMode::Check;
    std::string run_id = "single";
    std::string suite = "manual";
};
// Generate once, verify both algorithms, then write the selected CSV schema.
// Failed invocations throw; no fabricated distance or timing rows are produced.
void run_benchmark(const BenchmarkConfig& config, std::ostream& output);
}  // namespace project2
