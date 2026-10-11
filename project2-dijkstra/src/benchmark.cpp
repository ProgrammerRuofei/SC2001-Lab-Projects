#include "benchmark.hpp"
#include "scaffold.hpp"

namespace project2 {
void run_benchmark(const BenchmarkConfig& config, std::ostream& output) {
    // OWNER: Member C, after algorithm handoff.
    // TODO: generate once, convert both ways, compare full distances outside timing.
    // Check: print real results. Timing: fresh state, warmups, paired order,
    // steady_clock, stats=nullptr, result consumption/output after the clock stops.
    // Count: independent calls with fresh stats; never include these in timing CSV.
    // See docs/experiment-plan.md for column order and metadata.
    (void)config; (void)output;
    throw NotImplemented("Member C: benchmark/check/count pipeline");
}
}  // namespace project2
