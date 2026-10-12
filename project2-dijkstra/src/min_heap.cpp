#include "min_heap.hpp"

#include <stdexcept>
#include <utility>

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
    std::swap(heap_[left], heap_[right]);
    position_[heap_[left].vertex] = left;
    position_[heap_[right].vertex] = right;
}
void IndexedMinHeap::sift_up(std::size_t index) {
    while (index > 0) {
        const auto parent = (index - 1) / 2;
        if (!precedes(heap_[index], heap_[parent])) break;
        swap_entries(index, parent);
        index = parent;
    }
}
void IndexedMinHeap::sift_down(std::size_t index) {
    // Internal nodes occupy the first size()/2 positions.
    while (index < heap_.size() / 2) {
        auto child = 2 * index + 1;
        const auto right = child + 1;
        if (right < heap_.size() && precedes(heap_[right], heap_[child])) child = right;
        if (!precedes(heap_[child], heap_[index])) break;
        swap_entries(index, child);
        index = child;
    }
}
void IndexedMinHeap::push_or_decrease(Vertex vertex, Distance key) {
    if (vertex >= position_.size() || key < 0 || key >= kInfinity)
        throw std::invalid_argument("Invalid heap vertex or key");
    auto index = position_[vertex];
    if (index == kNoVertex) {
        index = heap_.size();
        heap_.push_back({vertex, key});
        position_[vertex] = index;
    } else {
        if (key >= heap_[index].key) return;
        heap_[index].key = key;
    }
    sift_up(index);
}
HeapEntry IndexedMinHeap::extract_min() {
    if (empty()) throw std::out_of_range("Cannot extract from an empty heap");
    const auto minimum = heap_.front();
    position_[minimum.vertex] = kNoVertex;
    if (heap_.size() == 1) {
        heap_.pop_back();
    } else {
        heap_.front() = heap_.back();
        heap_.pop_back();
        position_[heap_.front().vertex] = 0;
        sift_down(0);
    }
    return minimum;
}
}  // namespace project2
