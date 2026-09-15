CXX := c++
CXXFLAGS := -std=c++17 -Wall -Wextra -Wpedantic -O2
CPPFLAGS := -Iinclude
BUILD_DIR := build

.PHONY: all test clean

all: $(BUILD_DIR)/hybrid_sort

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BUILD_DIR)/hybrid_sort: src/main.cpp src/sorting.cpp include/sorting.hpp | $(BUILD_DIR)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) src/main.cpp src/sorting.cpp -o $@

$(BUILD_DIR)/test_sorting: tests/test_sorting.cpp src/sorting.cpp include/sorting.hpp | $(BUILD_DIR)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) tests/test_sorting.cpp src/sorting.cpp -o $@

test: $(BUILD_DIR)/test_sorting
	./$(BUILD_DIR)/test_sorting

clean:
	rm -rf $(BUILD_DIR)

