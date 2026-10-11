// Diagnostic-only global operator new/delete overrides.
// Counts heap allocation calls and bytes for the whole process, so we can
// compare original Merge Sort against Hybrid Merge Sort on the same input
// setup (identical input generation and one initial copy), isolating the
// difference caused by how many temporary vectors merge() constructs.

#include <cstdlib>
#include <new>

long long gNewCalls = 0;
long long gDeleteCalls = 0;
long long gBytesAllocated = 0;

void* operator new(std::size_t size) {
    ++gNewCalls;
    gBytesAllocated += static_cast<long long>(size);
    void* pointer = std::malloc(size == 0 ? 1 : size);
    if (pointer == nullptr) {
        throw std::bad_alloc();
    }
    return pointer;
}

void* operator new[](std::size_t size) {
    return ::operator new(size);
}

void operator delete(void* pointer) noexcept {
    ++gDeleteCalls;
    std::free(pointer);
}

void operator delete(void* pointer, std::size_t) noexcept {
    ++gDeleteCalls;
    std::free(pointer);
}

void operator delete[](void* pointer) noexcept {
    ::operator delete(pointer);
}

void operator delete[](void* pointer, std::size_t) noexcept {
    ::operator delete(pointer);
}
