#include "generation.hpp"
#include "scaffold.hpp"

namespace project2 {
EdgeListGraph generate_connected_graph(const GraphSpec& spec) {
    // OWNER: Member C. Teammates use examples.hpp until this is ready.
    // TODO C1: validate n/m/weight range and overflow-safe path bound.
    // TODO C2: seed RNG; shuffle vertices; add a spanning path for connectivity.
    // TODO C3: add distinct canonical pairs until exactly m edges exist.
    // TODO C4: generate weights, sort edges, document distribution/version.
    // TODO C5: test exact edge count, connectivity, seed reproduction and errors.
    (void)spec;
    throw NotImplemented("Member C: connected random graph generator");
}
}  // namespace project2
