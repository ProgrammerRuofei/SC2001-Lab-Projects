#pragma once

#include "types.hpp"

#include <vector>

namespace project2 {

struct HeapEntry {
    Vertex vertex;
    Distance key;
};

// Indexed binary min-heap: one entry per vertex, ordered by (key, vertex).
// Core heap operations remain TODOs; basic state accessors are provided.
class IndexedMinHeap {
public:
    explicit IndexedMinHeap(Vertex vertex_count);

    bool empty() const;
    std::size_t size() const;
    bool contains(Vertex vertex) const;

    // Insert if absent; decrease an existing key if smaller; otherwise no-op.
    // Reject invalid vertex IDs and keys outside [0, kInfinity).
    void push_or_decrease(Vertex vertex, Distance key);

    // Reject extraction from an empty heap.
    HeapEntry extract_min();

private:
    std::vector<HeapEntry> heap_;
    // position_[v] is kNoVertex when v has no heap entry.
    std::vector<std::size_t> position_;

    bool precedes(const HeapEntry& left, const HeapEntry& right) const;
    void swap_entries(std::size_t left, std::size_t right);
    void sift_up(std::size_t index);
    void sift_down(std::size_t index);
};

}  // namespace project2
