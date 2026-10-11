#include "min_heap.hpp"
#include "scaffold.hpp"

#include <stdexcept>

namespace project2 {
IndexedMinHeap::IndexedMinHeap(Vertex vertex_count)
    : position_(vertex_count, kNoVertex) {}
bool IndexedMinHeap::empty() const { return heap_.empty(); }
std::size_t IndexedMinHeap::size() const { return heap_.size(); }
bool IndexedMinHeap::contains(Vertex vertex) const {
    if (vertex >= position_.size()) throw std::invalid_argument("Invalid heap vertex");
    return position_[vertex] != kNoVertex;
}
bool IndexedMinHeap::precedes(const HeapEntry& a, const HeapEntry& b) const {
    return a.key < b.key || (a.key == b.key && a.vertex < b.vertex);
}
void IndexedMinHeap::swap_entries(std::size_t left, std::size_t right) {
    // OWNER: Member B. Exchange heap entries AND update both position values.
    (void)left; (void)right;
    throw NotImplemented("Member B: heap swap and position tracking");
}
void IndexedMinHeap::sift_up(std::size_t index) {
    // TODO: compare with parent while index > 0; swap until heap order holds.
    (void)index;
    throw NotImplemented("Member B: heap sift-up");
}
void IndexedMinHeap::sift_down(std::size_t index) {
    // TODO: choose smaller valid child; swap until heap order holds.
    (void)index;
    throw NotImplemented("Member B: heap sift-down");
}
void IndexedMinHeap::push_or_decrease(Vertex vertex, Distance key) {
    // TODO: reject invalid vertex/key; insert if absent or decrease existing key.
    // Equal/larger keys are no-ops. Restore order and preserve one entry per vertex.
    (void)vertex; (void)key;
    throw NotImplemented("Member B: heap insert/decrease-key");
}
HeapEntry IndexedMinHeap::extract_min() {
    // TODO: handle empty/single-entry heaps; replace root with last entry;
    // mark removed vertex absent, update new root position, then sift down.
    throw NotImplemented("Member B: heap extract-min");
}
}  // namespace project2
