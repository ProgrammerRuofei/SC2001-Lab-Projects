#include "dijkstra.hpp"
#include "scaffold.hpp"

namespace project2 {
DijkstraResult dijkstra_matrix(const MatrixGraph& graph, Vertex source,
                               OperationStats* stats) {
    // OWNER: Member A. Start with teaching_graph() and source 0.
    // TODO A1: validate source; initialize dist/parent/settled arrays.
    // TODO A2: scan all indices to select the minimum unsettled finite distance.
    //          Resolve equal distances by smaller vertex ID; stop at INF.
    // TODO A3: settle u; scan all n columns and relax eligible existing edges.
    //          Guard additions; update parents only on strict improvements.
    // TODO A4: optional counters follow docs/architecture.md; nullptr means off.
    // TODO A5: return real distances/parents and pass tests/test_matrix.cpp.
    (void)graph; (void)source; (void)stats;
    throw NotImplemented("Member A: matrix/array Dijkstra");
}
}  // namespace project2
