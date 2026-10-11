#include "dijkstra.hpp"
#include "min_heap.hpp"
#include "scaffold.hpp"

namespace project2 {
DijkstraResult dijkstra_heap(const ListGraph& graph, Vertex source,
                             OperationStats* stats) {
    // OWNER: Member B. Complete and independently test IndexedMinHeap first.
    // TODO B1: validate source; initialize arrays; insert source with key 0.
    // TODO B2: extract the minimum vertex and settle it.
    // TODO B3: scan actual neighbors, skip settled vertices, guard additions.
    // TODO B4: on every strict improvement, update dist/parent AND heap key.
    // TODO B5: collect optional counters; stop when heap is empty; return result.
    // One entry per vertex: do not introduce lazy deletion without updating docs.
    (void)graph; (void)source; (void)stats;
    throw NotImplemented("Member B: list/indexed-heap Dijkstra");
}
}  // namespace project2
