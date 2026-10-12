#include "generation.hpp"

#include <algorithm>
#include <functional>
#include <limits>
#include <numeric>
#include <random>
#include <stdexcept>
#include <unordered_set>
#include <utility>

namespace project2 {
namespace {
using Pair = std::pair<Vertex, Vertex>;
struct PairHash {
    std::size_t operator()(const Pair& pair) const {
        const auto first = std::hash<Vertex>{}(pair.first);
        return first ^ (std::hash<Vertex>{}(pair.second) +
                        std::size_t{0x9e3779b9} + (first << 6) + (first >> 2));
    }
};

std::size_t maximum_edges(Vertex n) {
    if (n == 1) return 0;
    // Divide before multiplying to avoid overflow in n*(n-1)/2.
    auto a = n;
    auto b = n - 1;
    if (a % 2 == 0) a /= 2;
    else b /= 2;
    if (a > std::numeric_limits<std::size_t>::max() / b)
        throw std::invalid_argument("Vertex count exceeds representable edge capacity");
    return a * b;
}
}  // namespace

EdgeListGraph generate_connected_graph(const GraphSpec& spec) {
    const auto n = spec.vertex_count;
    if (n == 0) throw std::invalid_argument("Graph needs at least one vertex");
    if (spec.weight_min < 0 || spec.weight_max < spec.weight_min ||
        spec.weight_max >= kInfinity)
        throw std::invalid_argument("Invalid weight range");
    if (spec.weight_max > 0 && n - 1 >
        static_cast<Vertex>((kInfinity - 1) / spec.weight_max))
        throw std::invalid_argument("Simple-path distance bound exceeds INF");
    const auto capacity = maximum_edges(n);
    if (spec.edge_count < n - 1 || spec.edge_count > capacity)
        throw std::invalid_argument("Edge count cannot form a simple connected graph");

    std::mt19937_64 rng(spec.graph_seed);
    std::vector<Vertex> vertices(n);
    std::iota(vertices.begin(), vertices.end(), Vertex{0});
    std::shuffle(vertices.begin(), vertices.end(), rng);
    std::vector<Pair> pairs;
    pairs.reserve(spec.edge_count);
    std::unordered_set<Pair, PairHash> chosen;
    chosen.reserve(spec.edge_count);
    auto add = [&](Vertex u, Vertex v) {
        if (u == v) return;
        if (u > v) std::swap(u, v);
        if (chosen.emplace(u, v).second) pairs.emplace_back(u, v);
    };

    // A spanning path guarantees that every vertex is reachable.
    for (Vertex i = 1; i < n; ++i) add(vertices[i - 1], vertices[i]);
    const auto extra = spec.edge_count - pairs.size();
    const auto remaining = capacity - pairs.size();
    if (extra > remaining / 4) {
        // Dense inputs: sample without replacement instead of rejecting many pairs.
        std::vector<Pair> candidates;
        candidates.reserve(remaining);
        for (Vertex u = 0; u < n; ++u)
            for (Vertex v = u + 1; v < n; ++v)
                if (chosen.find({u, v}) == chosen.end()) candidates.emplace_back(u, v);
        std::shuffle(candidates.begin(), candidates.end(), rng);
        for (std::size_t i = 0; i < extra; ++i) pairs.push_back(candidates[i]);
    } else if (extra > 0) {
        // Sparse inputs: avoid allocating an O(n²) candidate array.
        std::uniform_int_distribution<Vertex> vertex(0, n - 1);
        while (pairs.size() < spec.edge_count) {
            const auto u = vertex(rng);
            const auto v = vertex(rng);
            add(u, v);
        }
    }

    std::sort(pairs.begin(), pairs.end());
    std::uniform_int_distribution<Weight> weight(spec.weight_min, spec.weight_max);
    EdgeListGraph graph{n, {}};
    graph.edges.reserve(spec.edge_count);
    for (const auto& pair : pairs)
        graph.edges.push_back({pair.first, pair.second, weight(rng)});
    return graph;
}
}  // namespace project2
